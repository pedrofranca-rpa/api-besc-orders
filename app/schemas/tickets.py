from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class TicketBase(BaseModel):
    order_id: int
    ticket_number: Optional[int] = None
    opened_at: Optional[date] = None
    closed_at: Optional[date] = None
    status_id: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TicketCreate(TicketBase):
    pass


class TicketResponse(TicketBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
