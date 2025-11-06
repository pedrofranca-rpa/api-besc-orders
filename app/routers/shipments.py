from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.shipments import (
    create_shipment,
    get_shipment,
    update_shipment,
    delete_shipment,
)
from app.schemas.shipments import ShipmentCreate, ShipmentResponse

router = APIRouter(prefix="/api/shipments", tags=["Shipments"])


# 🟢 Create shipment
@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment_route(
    shipment: ShipmentCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new shipment record.
    """
    return await create_shipment(db, shipment)


# 🔵 Get shipment by ID
@router.get("/{id}", response_model=ShipmentResponse, status_code=status.HTTP_200_OK)
async def get_shipment_route(id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a shipment record by its ID.
    """
    return await get_shipment(db, id)


# 🟣 Update shipment
@router.put("/{id}", response_model=ShipmentResponse, status_code=status.HTTP_200_OK)
async def update_shipment_route(
    id: int, shipment: ShipmentCreate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing shipment record.
    """
    return await update_shipment(db, id, shipment)


# 🔴 Delete shipment
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment_route(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a shipment record by its ID.
    """
    deleted = await delete_shipment(db, id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found."
        )
    return None
