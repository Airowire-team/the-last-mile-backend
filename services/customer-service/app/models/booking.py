
import uuid
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    Text
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from shared.database.postgres import Base
class Booking(Base):

    __tablename__ = "bookings"

    # Primary key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    # Booking information
    ticket_no = Column(Text, unique=True, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    customer_name = Column(Text, nullable=True)
    service_slug = Column(Text,nullable=False,default="field-engineer-support")
    title = Column(Text, nullable=False)
    priority = Column(Text,nullable=False,default="Medium")
    city = Column(Text, nullable=True)
    site_address = Column(Text, nullable=True)
    engineer_id = Column(UUID(as_uuid=True), nullable=True)
    engineer_name = Column(Text,nullable=False,default="Unassigned")
    engineer_phone = Column(Text, nullable=True)
    progress = Column(Integer, default=12, nullable=False)
    status = Column(Text,nullable=False,default="Open")
    total = Column(Numeric(12, 2), nullable=True)
    amount_paid = Column(Numeric(12, 2), nullable=True)
    payment_status = Column(Text, nullable=True)
    invoice_no = Column(Text, nullable=True)
    details = Column(JSONB,nullable=False,default=dict)
    last_contact = Column(Text, nullable=True)
    customer_rating = Column(Integer, nullable=True)
    customer_feedback = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Audit information
    created_by = Column(UUID(as_uuid=True), nullable=True)

    updated_by = Column(UUID(as_uuid=True), nullable=True)
