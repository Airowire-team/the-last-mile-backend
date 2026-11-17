# import uuid
# from fastapi import HTTPException
# from sqlalchemy.orm import Session
# from app.repositories.booking_repository import BookingRepository
# from app.schemas.booking import BookingCreate, BookingUpdate
# _repository = BookingRepository()


# def create_booking(db: Session, data: BookingCreate):
#     booking_data = data.model_dump()
#     booking_data["ticket_no"] = f"BK-{uuid.uuid4().hex.upper()}"
#     return _repository.create(db, booking_data)


# def get_all_bookings(db: Session, skip: int, limit: int):
#     return _repository.get_all(db, skip, limit)


# def get_booking_by_id(db: Session, booking_id: uuid.UUID):
#     return _repository.get_by_id(db, booking_id)


# def update_booking(db: Session, booking_id: uuid.UUID, data: BookingUpdate):
#     booking = _repository.get_by_id(db, booking_id)
#     if booking is None:
#         return None

#     changes = data.model_dump(exclude_unset=True)
#     required_fields = {
#         "title", "service_slug", "priority", "engineer_name",
#         "progress", "details", "status",
#     }
#     for field in required_fields.intersection(changes):
#         if changes[field] is None:
#             raise HTTPException(status_code=422, detail=f"{field} cannot be null")

#     return _repository.update(db, booking, changes)


# def delete_booking(db: Session, booking_id: uuid.UUID):
#     booking = _repository.get_by_id(db, booking_id)
#     if booking is None:
#         return False
#     _repository.delete(db, booking)
#     return True

import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.booking_repository import BookingRepository
from app.schemas.booking import BookingCreate, BookingUpdate

_repository = BookingRepository()


# CREATE BOOKING
def create_booking(db: Session, data: BookingCreate):

    booking_data = data.model_dump()

    # Generate unique ticket number
    booking_data["ticket_no"] = (
        f"BK-{uuid.uuid4().hex.upper()}"
    )

    return _repository.create(db, booking_data)


# GET ALL BOOKINGS
def get_all_bookings(
    db: Session,
    skip: int,
    limit: int
):
    return _repository.get_all(db, skip, limit)


# GET BOOKING BY ID
def get_booking_by_id(db: Session, booking_id: uuid.UUID):

    return _repository.get_by_id(db, booking_id)


# UPDATE BOOKING
def update_booking(
    db: Session,
    booking_id: uuid.UUID,
    data: BookingUpdate
):

    booking = _repository.get_by_id(db, booking_id)

    if booking is None:
        return None

    changes = data.model_dump(exclude_unset=True)

    # Fields that cannot be NULL
    required_fields = {
        "title",
        "service_slug",
        "priority",
        "engineer_name",
        "progress",
        "status",
        "details"
    }

    for field in required_fields.intersection(changes):

        if changes[field] is None:

            raise HTTPException(
                status_code=422,
                detail=f"{field} cannot be null"
            )

    return _repository.update(db, booking, changes)


# DELETE BOOKING
def delete_booking(db: Session, booking_id: uuid.UUID):

    booking = _repository.get_by_id(db, booking_id)

    if booking is None:
        return False

    _repository.delete(db, booking)

    return True
