# app/services/icms.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.taxes.icms import ICMS as ICMSModel
from app.schemas.taxes.icms import ICMSCreate, ICMSResponse
from fastapi import HTTPException


async def create_icms(db: AsyncSession, icms_in: ICMSCreate) -> ICMSResponse:
    db_icms = ICMSModel(**icms_in)
    db.add(db_icms)
    await db.commit()
    await db.refresh(db_icms)

    return ICMSResponse.model_validate(db_icms, from_attributes=True)


async def get_icms(db: AsyncSession, icms_id: int) -> ICMSResponse:
    result = await db.execute(select(ICMSModel).filter(ICMSModel.id == icms_id))
    icms = result.scalar_one_or_none()
    if not icms:
        raise HTTPException(404, "ICMS não encontrado")
    return ICMSResponse.model_validate(icms, from_attributes=True)
