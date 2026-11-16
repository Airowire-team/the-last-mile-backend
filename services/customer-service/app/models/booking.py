import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, Numeric, Table, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from shared.database.postgres import Base


# Reference metadata is separate so create_all cannot create incomplete external tables.
reference_metadata = MetaData()
profiles = Table("profiles", reference_metadata, Column("id", UUID(as_uuid=True), primary_key=True))
engineers = Table("engineers", reference_metadata, Column("id", UUID(as_uuid=True), primary_key=True))


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticket_no = Column(Text, nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey(profiles.c.id))
    customer_name = Column(Text)
    service_slug = Column(Text)
    title = Column(Text)
    priority = Column(Text)
    city = Column(Text)
    site_address = Column(Text)
    engineer_id = Column(UUID(as_uuid=True), ForeignKey(engineers.c.id))
    engineer_name = Column(Text)
    engineer_phone = Column(Text)
    progress = Column(Integer, default=0)
    status = Column(Text)
    total = Column(Numeric(12, 2))
    details = Column(JSONB)
    last_contact = Column(Text)
    customer_rating = Column(Integer)
    customer_feedback = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    payment_status = Column(Text)
    amount_paid = Column(Numeric(12, 2))
    invoice_no = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))
