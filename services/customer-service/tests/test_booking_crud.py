import asyncio
import json
import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.compiler import compiles, deregister
from sqlalchemy.orm import Session

from app.main import app
from app.models.booking import Booking
from app.repositories.booking_repository import BookingRepository
from app.services import booking_service
from shared.database.postgres import get_db


class MemoryRepository:
    def __init__(self):
        self.bookings = {}

    def create(self, db, booking_data):
        now = datetime.now(timezone.utc)
        booking = Booking(
            id=uuid.uuid4(),
            created_at=now,
            updated_at=now,
            **booking_data,
        )
        self.bookings[booking.id] = booking
        return booking

    def get_all(self, db, skip, limit):
        return list(self.bookings.values())[skip:skip + limit]

    def get_by_id(self, db, booking_id):
        return self.bookings.get(booking_id)

    def update(self, db, booking, changes):
        for field, value in changes.items():
            setattr(booking, field, value)
        return booking

    def delete(self, db, booking):
        del self.bookings[booking.id]


@pytest.fixture
def api(monkeypatch):
    monkeypatch.setattr(booking_service, "_repository", MemoryRepository())
    app.dependency_overrides[get_db] = lambda: None
    yield
    app.dependency_overrides.pop(get_db, None)


def request(method, path, body=None, query_string=b""):
    messages = []
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": query_string,
        "headers": [(b"content-type", b"application/json")],
        "client": ("127.0.0.1", 1234),
        "server": ("127.0.0.1", 8000),
    }

    async def receive():
        return {
            "type": "http.request",
            "body": json.dumps(body).encode() if body is not None else b"",
            "more_body": False,
        }

    async def send(message):
        messages.append(message)

    asyncio.run(app(scope, receive, send))
    return messages[0]["status"], json.loads(messages[1]["body"])


def test_booking_crud(api):
    status, created = request("POST", "/api/bookings", {"title": "Network issue"})
    assert status == 201
    assert created["title"] == "Network issue"
    assert created["user_id"] is None
    assert created["ticket_no"].startswith("BK-")

    path = "/api/bookings/" + created["id"]
    status, retrieved = request("GET", path)
    assert status == 200
    assert retrieved["id"] == created["id"]

    status, listed = request("GET", "/api/bookings")
    assert status == 200
    assert [booking["id"] for booking in listed] == [created["id"]]

    status, updated = request("PUT", path, {"title": "Router issue"})
    assert status == 200
    assert updated["title"] == "Router issue"
    assert updated["priority"] == created["priority"]

    status, _ = request("DELETE", path)
    assert status == 200
    assert request("GET", path)[0] == 404


def test_booking_validation(api):
    status, created = request("POST", "/api/bookings", {"title": "Network issue"})
    assert status == 201
    path = "/api/bookings/" + created["id"]
    assert request("PUT", path, {"title": None})[0] == 422
    assert request("GET", "/api/bookings", query_string=b"skip=-1")[0] == 422
    assert request("GET", "/api/bookings/not-a-uuid")[0] == 400


def test_repository_crud_with_isolated_database():
    @compiles(JSONB, "sqlite")
    def compile_jsonb(type_, compiler, **kwargs):
        return "JSON"

    engine = create_engine("sqlite://")
    try:
        metadata = MetaData()
        for name in ("profiles", "engineers"):
            Table(name, metadata, Column("id", UUID(as_uuid=True), primary_key=True))
        Booking.__table__.to_metadata(metadata)
        metadata.create_all(engine)

        repository = BookingRepository()
        with Session(engine) as db:
            booking = repository.create(
                db, {"ticket_no": "BK-TEST", "title": "Original", "details": {}}
            )
            booking_id = booking.id
            assert repository.get_all(db, 0, 10)[0].id == booking_id
            assert repository.get_all(db, 1, 10) == []
            assert repository.get_by_id(db, booking_id).title == "Original"
            repository.update(db, booking, {"title": "Updated"})
            assert repository.get_by_id(db, booking_id).title == "Updated"
            repository.delete(db, booking)
            assert repository.get_by_id(db, booking_id) is None
    finally:
        engine.dispose()
        deregister(JSONB)
