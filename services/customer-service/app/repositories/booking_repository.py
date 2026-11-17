# from uuid import UUID

# from sqlalchemy.orm import Session

# from app.models.booking import Booking


# class BookingRepository:
#     def create(self, db: Session, booking_data: dict):
#         booking = Booking(**booking_data)
#         db.add(booking)
#         db.commit()
#         db.refresh(booking)
#         return booking

#     def get_all(self, db: Session, skip: int, limit: int):
#         return (
#             db.query(Booking)
#             .order_by(Booking.created_at.desc(), Booking.id)
#             .offset(skip)
#             .limit(limit)
#             .all()
#         )

#     def get_by_id(self, db: Session, booking_id: UUID):
#         return db.query(Booking).filter(Booking.id == booking_id).first()

#     def update(self, db: Session, booking: Booking, changes: dict):
#         for field, value in changes.items():
#             setattr(booking, field, value)
#         db.commit()
#         db.refresh(booking)
#         return booking

#     def delete(self, db: Session, booking: Booking):
#         db.delete(booking)
#         db.commit()

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.booking import Booking


class BookingRepository:

    # CREATE
    def create(self, db: Session, booking_data: dict):

        booking = Booking(**booking_data)

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return booking

    # GET ALL
    def get_all(self, db: Session, skip: int, limit: int):

        return (
            db.query(Booking)
            .filter()
            .order_by(Booking.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    # GET BY ID
    def get_by_id(self, db: Session, booking_id: UUID):

        return (
            db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

    # UPDATE
    def update(
        self,
        db: Session,
        booking: Booking,
        changes: dict
    ):

        for field, value in changes.items():

            setattr(booking, field, value)

        db.commit()
        db.refresh(booking)

        return booking

    # DELETE
    def delete(self, db: Session, booking: Booking):

        db.delete(booking)
        db.commit()

        return True
