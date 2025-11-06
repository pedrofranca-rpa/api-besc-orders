from pydantic import BaseModel, ConfigDict


class IPIBase(BaseModel):
    value: float
    rate: float
    base_amount: float

    model_config = ConfigDict(from_attributes=True)


class IPICreate(IPIBase):
    pass


class IPIResponse(IPIBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
