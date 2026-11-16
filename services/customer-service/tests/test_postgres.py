import pytest
from sqlalchemy import text

from shared.database.postgres import _session_factory, get_db


@pytest.fixture(autouse=True)
def clear_session_factory():
    _session_factory.cache_clear()
    yield
    _session_factory.cache_clear()


def test_missing_database_url_reports_configuration_error(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="DATABASE_URL must be set"):
        next(get_db())


def test_session_closes_and_rolls_back_uncommitted_work(monkeypatch, tmp_path):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{(tmp_path / 'test.db').as_posix()}")
    dependency = get_db()
    db = next(dependency)
    db.execute(text("CREATE TABLE bookings (id INTEGER PRIMARY KEY)"))
    db.commit()
    db.execute(text("INSERT INTO bookings (id) VALUES (1)"))
    dependency.close()

    with _session_factory()() as db:
        assert db.execute(text("SELECT COUNT(*) FROM bookings")).scalar_one() == 0
