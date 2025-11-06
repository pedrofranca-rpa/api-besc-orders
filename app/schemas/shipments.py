from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class ShipmentBase(BaseModel):
    status_id: Optional[int] = None
    description: str
    tracking_number: Optional[str] = None
    shipment_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentResponse(ShipmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
