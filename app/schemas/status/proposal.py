from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProposalStatusBase(BaseModel):
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProposalStatusCreate(ProposalStatusBase):
    pass


class ProposalStatus(ProposalStatusBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
