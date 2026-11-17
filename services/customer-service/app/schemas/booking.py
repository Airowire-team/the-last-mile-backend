

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class BookingCreate(BaseModel):

    user_id: Optional[UUID] = None

    customer_name: Optional[str] = None

    service_slug: str = "field-engineer-support"

    title: str

    priority: str = "Medium"

    city: Optional[str] = None

    site_address: Optional[str] = None

    engineer_id: Optional[UUID] = None

    engineer_name: str = "Unassigned"

    engineer_phone: Optional[str] = None

    progress: int = Field(default=12, ge=0, le=100)

    status: str = "Open"

    total: Optional[Decimal] = Field(default=None, ge=0)

    amount_paid: Optional[Decimal] = Field(default=None, ge=0)

    payment_status: Optional[str] = None

    invoice_no: Optional[str] = None

    details: dict[str, Any] = Field(default_factory=dict)

    last_contact: Optional[str] = None

    customer_rating: Optional[int] = Field(default=None, ge=1, le=5)

    customer_feedback: Optional[str] = None

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    created_by: Optional[UUID] = None


class BookingUpdate(BaseModel):

    user_id: Optional[UUID] = None

    customer_name: Optional[str] = None

    service_slug: Optional[str] = None

    title: Optional[str] = None

    priority: Optional[str] = None

    city: Optional[str] = None

    site_address: Optional[str] = None

    engineer_id: Optional[UUID] = None

    engineer_name: Optional[str] = None

    engineer_phone: Optional[str] = None

    progress: Optional[int] = Field(default=None, ge=0, le=100)

    status: Optional[str] = None

    total: Optional[Decimal] = Field(default=None, ge=0)

    amount_paid: Optional[Decimal] = Field(default=None, ge=0)

    payment_status: Optional[str] = None

    invoice_no: Optional[str] = None

    details: Optional[dict[str, Any]] = None

    last_contact: Optional[str] = None

    customer_rating: Optional[int] = Field(default=None, ge=1, le=5)

    customer_feedback: Optional[str] = None

    started_at: Optional[datetime] = None

    completed_at: Optional[datetime] = None

    updated_by: Optional[UUID] = None


class BookingResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    ticket_no: str

    user_id: Optional[UUID]

    customer_name: Optional[str]

    service_slug: str

    title: str

    priority: str

    city: Optional[str]

    site_address: Optional[str]

    engineer_id: Optional[UUID]

    engineer_name: str

    engineer_phone: Optional[str]

    progress: int

    status: str

    total: Optional[Decimal]

    amount_paid: Optional[Decimal]

    payment_status: Optional[str]

    invoice_no: Optional[str]

    details: dict[str, Any]

    last_contact: Optional[str]

    customer_rating: Optional[int]

    customer_feedback: Optional[str]

    started_at: Optional[datetime]

    completed_at: Optional[datetime]

    created_at: datetime

    updated_at: datetime

    created_by: Optional[UUID]

    updated_by: Optional[UUID]
