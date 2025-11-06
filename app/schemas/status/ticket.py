from pydantic import BaseModel, ConfigDict
from typing import Optional


class TicketStatusBase(BaseModel):
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class TicketStatusCreate(TicketStatusBase):
    pass


class TicketStatus(TicketStatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
