from pydantic import BaseModel, ConfigDict
from typing import Optional

from app.schemas.taxes.icms import ICMSBase, ICMSCreate
from app.schemas.taxes.ipi import IPIBase, IPICreate


# =====================================================
# 🔹 Schemas base
# =====================================================
class TaxBase(BaseModel):
    id_icms: Optional[int] = None
    id_ipi: Optional[int] = None


# =====================================================
# 🔹 Schema de criação (entrada)
# =====================================================
class TaxCreate(BaseModel):
    icms: Optional[ICMSCreate] = None
    ipi: Optional[IPICreate] = None


# =====================================================
# 🔹 Schema principal (resposta simplificada)
# =====================================================
class Tax(BaseModel):
    id: int
    id_icms: Optional[int] = None
    id_ipi: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# =====================================================
# 🔹 Schema detalhado (resposta completa com relações)
# =====================================================
class TaxResponse(BaseModel):
    id: int
    icms: Optional[ICMSBase] = None
    ipi: Optional[IPIBase] = None

    model_config = ConfigDict(from_attributes=True)
