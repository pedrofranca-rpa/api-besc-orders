from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductBase(BaseModel):
    order_id: Optional[int] = None
    item: Optional[str] = None
    tax_id: Optional[int] = None
    part_number: Optional[str] = None
    description: Optional[str] = None
    ncm_code: Optional[str] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    quantity: Optional[int] = None
    material: Optional[str] = None
    origin: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
