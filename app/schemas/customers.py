from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    name: str
    tax_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
