
# import logging

# from fastapi import APIRouter, Depends, HTTPException, Query, status
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import SQLAlchemyError

# from shared.database.postgres import get_db

# from app.schemas.booking import (
#     BookingCreate,
#     BookingUpdate,
#     BookingResponse
# )

# from app.services import booking_service


# logger = logging.getLogger(__name__)

# router = APIRouter(
#     prefix="/bookings",
#     tags=["Bookings"]
# )


# # CREATE BOOKING
# @router.post(
#     "",
#     response_model=BookingResponse,
#     status_code=status.HTTP_201_CREATED
# )
# def create_booking(
#     booking_data: BookingCreate,
#     db: Session = Depends(get_db)
# ):
#     try:
#         booking = booking_service.create_booking(
#             db,
#             booking_data
#         )
#         return booking

#     except SQLAlchemyError as e:
#         db.rollback()
#         logger.exception("Database error creating booking")

#         raise HTTPException(
#             status_code=500,
#             detail="Database error creating booking"
#         ) from e


# # GET ALL BOOKINGS
# @router.get("", response_model=list[BookingResponse])
# def get_all_bookings(
#     skip: int = Query(default=0, ge=0),
#     limit: int = Query(default=100, ge=1),
#     db: Session = Depends(get_db)
# ):
#     return booking_service.get_all_bookings(
#         db, skip, limit
#     )


# # GET BOOKING BY ID
# @router.get("/{booking_id}", response_model=BookingResponse)
# def get_booking(
#     booking_id: str,
#     db: Session = Depends(get_db)
# ):
#     from uuid import UUID

#     try:
#         booking_id = UUID(booking_id)
#     except ValueError:
#         raise HTTPException(400, "Invalid booking ID")

#     booking = booking_service.get_booking_by_id(
#         db, booking_id
#     )

#     if not booking:
#         raise HTTPException(404, "Booking not found")

#     return booking


# # UPDATE BOOKING
# @router.put("/{booking_id}", response_model=BookingResponse)
# def update_booking(
#     booking_id: str,
#     booking_data: BookingUpdate,
#     db: Session = Depends(get_db)
# ):
#     from uuid import UUID

#     try:
#         booking_id = UUID(booking_id)

#         booking = booking_service.update_booking(
#             db, booking_id, booking_data
#         )

#         if not booking:
#             raise HTTPException(404, "Booking not found")

#         return booking

#     except ValueError:
#         raise HTTPException(400, "Invalid booking ID")

#     except HTTPException:
#         raise

#     except SQLAlchemyError:
#         db.rollback()
#         logger.exception("Booking update failed")
#         raise HTTPException(500, "Failed to update booking")


# # DELETE BOOKING
# @router.delete("/{booking_id}")
# def delete_booking(
#     booking_id: str,
#     db: Session = Depends(get_db)
# ):
#     from uuid import UUID

#     try:
#         booking_id = UUID(booking_id)

#         result = booking_service.delete_booking(
#             db, booking_id
#         )

#         if not result:
#             raise HTTPException(404, "Booking not found")

#         return {
#             "status": "success",
#             "message": "Booking deleted successfully"
#         }

#     except ValueError:
#         raise HTTPException(400, "Invalid booking ID")

#     except HTTPException:
#         raise

#     except SQLAlchemyError:
#         db.rollback()
#         logger.exception("Booking deletion failed")
#         raise HTTPException(500, "Failed to delete booking")

import logging

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from shared.database.postgres import get_db

from app.schemas.booking import (
    BookingCreate,
    BookingUpdate,
    BookingResponse
)

from app.services import booking_service


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# CREATE BOOKING
@router.post("", status_code=status.HTTP_201_CREATED)
def create_booking(
    data: BookingCreate,
    db: Session = Depends(get_db)
):
    booking = booking_service.create_booking(
        db, data
    )

    return {
        "id": str(booking.id),
        "message": "Booking service created successfully"
    }
# GET ALL BOOKINGS
@router.get(
    "",
    response_model=list[BookingResponse]
)
def get_all_bookings(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db)
):

    return booking_service.get_all_bookings(
        db,
        skip,
        limit
    )


# GET BOOKING BY ID
@router.get(
    "/{booking_id}",
    response_model=BookingResponse
)
def get_booking(
    booking_id: UUID,
    db: Session = Depends(get_db)
):

    booking = booking_service.get_booking_by_id(
        db,
        booking_id
    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking not found"
        )

    return booking


# UPDATE BOOKING

# UPDATE BOOKING
@router.put("/{booking_id}")
def update_booking(
    booking_id: UUID,
    booking_data: BookingUpdate,
    db: Session = Depends(get_db)
):
    try:
        booking = booking_service.update_booking(
            db,
            booking_id,
            booking_data
        )

        if not booking:
            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return {
            "message": "Booking updated successfully"
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        db.rollback()

        logger.exception("Booking update failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to update booking"
        ) from e


# DELETE BOOKING
@router.delete("/{booking_id}")
def delete_booking(
    booking_id: UUID,
    db: Session = Depends(get_db)
):

    try:

        result = booking_service.delete_booking(
            db,
            booking_id
        )

        if not result:

            raise HTTPException(
                status_code=404,
                detail="Booking not found"
            )

        return {
            "status": "success",
            "message": "Booking deleted successfully"
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:

        db.rollback()

        logger.exception("Booking deletion failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to delete booking"
        ) from e
