from pydantic import BaseModel, ConfigDict
from typing import Optional


class ShipmentStatusBase(BaseModel):
    description: str

    model_config = ConfigDict(from_attributes=True)


class ShipmentStatusCreate(ShipmentStatusBase):
    pass


class ShipmentStatus(ShipmentStatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
