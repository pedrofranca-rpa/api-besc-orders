from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.taxs import (
    create_tax_record_with_details,
    get_tax_record_with_details,
)
from app.schemas.taxs import TaxCreate, TaxResponse

router = APIRouter(prefix="/api/tax-records", tags=["Tax Records"])


@router.post("/", response_model=TaxResponse, status_code=status.HTTP_201_CREATED)
async def create_tax_record(data: TaxCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates a tax record linked to ICMS and/or IPI (both optional).
    """

    # If neither ICMS nor IPI is provided, raise an error
    if not data.icms and not data.ipi:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="ICMS ou IPI deve ser passado!",
        )

    # Convert Pydantic models to dicts (or None)
    icms_data = data.icms.model_dump() if data.icms else None
    ipi_data = data.ipi.model_dump() if data.ipi else None

    # Create the tax record
    tax_record = await create_tax_record_with_details(db, icms_data, ipi_data)
    return tax_record


@router.get("/{id}", response_model=TaxResponse)
async def get_tax_record(id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieves a tax record and its details (ICMS and IPI).
    """
    return await get_tax_record_with_details(db, id)
