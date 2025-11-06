# app/services/ipi.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.taxes.ipi import IPI as IPIModel
from app.schemas.taxes.ipi import IPICreate, IPIResponse
from fastapi import HTTPException


async def create_ipi(db: AsyncSession, ipi_in: IPICreate) -> IPIResponse:
    db_ipi = IPIModel(**ipi_in)
    db.add(db_ipi)
    await db.commit()
    await db.refresh(db_ipi)
    return IPIResponse.model_validate(db_ipi, from_attributes=True)


async def get_ipi(db: AsyncSession, ipi_id: int) -> IPIResponse:
    result = await db.execute(select(IPIModel).filter(IPIResponse.id == ipi_id))
    ipi = result.scalar_one_or_none()
    if not ipi:
        raise HTTPException(404, "IPI não encontrado")

    return IPIResponse.model_validate(ipi, from_attributes=True)
