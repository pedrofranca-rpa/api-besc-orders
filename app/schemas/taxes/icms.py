from pydantic import BaseModel, ConfigDict


class ICMSBase(BaseModel):
    value: float
    rate: float
    base_amount: float

    model_config = ConfigDict(from_attributes=True)


class ICMSCreate(ICMSBase):
    pass


class ICMSResponse(ICMSBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
