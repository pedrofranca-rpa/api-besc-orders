from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models.taxs import Tax as TaxRecordModel

from app.schemas.taxs import TaxResponse
from app.services.taxes.icms import create_icms, get_icms
from app.services.taxes.ipi import create_ipi, get_ipi


async def create_tax_record_with_details(
    db: AsyncSession, icms_data: dict | None = None, ipi_data: dict | None = None
) -> TaxResponse:
    """
    Creates a complete tax record, optionally including ICMS and IPI.

    Args:
        db: Asynchronous database session
        icms_data: Optional data for ICMS
        ipi_data: Optional data for IPI

    Returns:
        TaxResponse: Complete record with relationships
    """

    icms_id = None
    ipi_id = None

    # 1️⃣ Create ICMS if provided
    if icms_data and any(v is not None for v in icms_data.values()):
        icms = await create_icms(db, icms_data)
        icms_id = icms.id

    # 2️⃣ Create IPI if provided
    if ipi_data and any(v is not None for v in ipi_data.values()):
        ipi = await create_ipi(db, ipi_data)
        ipi_id = ipi.id

    # 3️⃣ Create the tax record (even if both are None)
    tax_record = TaxRecordModel(icms_id=icms_id, ipi_id=ipi_id)
    db.add(tax_record)
    await db.commit()
    await db.refresh(tax_record)

    # 4️⃣ Reload with relationships
    result = await db.execute(
        select(TaxRecordModel)
        .options(selectinload(TaxRecordModel.icms), selectinload(TaxRecordModel.ipi))
        .where(TaxRecordModel.id == tax_record.id)
    )

    tax_record_full = result.scalars().first()
    if not tax_record_full:
        raise HTTPException(500, "Error loading tax record after creation.")

    # 5️⃣ Return validated Pydantic schema
    return TaxResponse.model_validate(tax_record_full, from_attributes=True)


async def get_tax_record_with_details(db: AsyncSession, tax_record_id: int):
    """
    Retrieves a tax record by ID, including ICMS and IPI details.
    """
    result = await db.execute(
        select(TaxRecordModel).filter(TaxRecordModel.id == tax_record_id)
    )
    tax_record = result.scalar_one_or_none()
    if not tax_record:
        raise HTTPException(404, "Tax record not found.")

    icms = await get_icms(db, tax_record.icms_id)
    ipi = await get_ipi(db, tax_record.ipi_id)

    return {"tax_record_id": tax_record.id, "icms": icms, "ipi": ipi}
