from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime


class PaymentBase(BaseModel):
    payment_date: Optional[date] = None
    billing_until: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


class PaymentCreate(PaymentBase):
    pass


class PaymentResponse(PaymentBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
