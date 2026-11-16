
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Any
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class BookingCreate(BaseModel):
    title: str
    service_slug: str = "field-engineer-support"
    priority: str = "Medium"
    city: Optional[str] = None
    customer_name: Optional[str] = None
    site_address: Optional[str] = None
    engineer_name: str = "Unassigned"
    engineer_phone: Optional[str] = None
    progress: int = Field(default=12, ge=0, le=100)
    total: Optional[Decimal] = Field(default=None, ge=0)
    details: dict[str, Any] = Field(default_factory=dict)
    last_contact: Optional[str] = None
    status: str = "Open"
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None


class BookingUpdate(BaseModel):
    title: Optional[str] = None
    service_slug: Optional[str] = None
    priority: Optional[str] = None
    city: Optional[str] = None
    customer_name: Optional[str] = None
    site_address: Optional[str] = None
    engineer_name: Optional[str] = None
    engineer_phone: Optional[str] = None
    progress: Optional[int] = Field(default=None, ge=0, le=100)
    total: Optional[Decimal] = Field(default=None, ge=0)
    details: Optional[dict[str, Any]] = None
    last_contact: Optional[str] = None
    status: Optional[str] = None
    updated_by: Optional[UUID] = None


class BookingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    ticket_no: str
    user_id: Optional[UUID]
    service_slug: str
    title: str
    priority: str
    city: Optional[str]
    customer_name: Optional[str]
    site_address: Optional[str]
    engineer_name: str
    engineer_phone: Optional[str]
    progress: int
    total: Optional[Decimal]
    details: dict[str, Any]
    last_contact: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    created_by: Optional[UUID]
    updated_by: Optional[UUID]
