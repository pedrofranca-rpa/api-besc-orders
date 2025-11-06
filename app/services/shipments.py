from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi import HTTPException, status

from app.models.shipments import Shipment as ShipmentModel
from app.schemas.shipments import ShipmentCreate, ShipmentResponse


# 🟢 Create a new shipment
async def create_shipment(
    db: AsyncSession, shipment_in: ShipmentCreate
) -> ShipmentResponse:
    """
    Create a new shipment record.
    """
    db_shipment = ShipmentModel(**shipment_in.model_dump())
    db.add(db_shipment)
    await db.commit()
    await db.refresh(db_shipment)
    return ShipmentResponse.model_validate(db_shipment, from_attributes=True)


# 🔵 Get a shipment by ID
async def get_shipment(db: AsyncSession, shipment_id: int) -> ShipmentResponse:
    """
    Retrieve a shipment record by its ID.
    """
    result = await db.execute(
        select(ShipmentModel).filter(ShipmentModel.id == shipment_id)
    )
    shipment = result.scalar_one_or_none()

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found."
        )

    return ShipmentResponse.model_validate(shipment, from_attributes=True)


# 🟣 Update a shipment
async def update_shipment(
    db: AsyncSession, shipment_id: int, shipment_in: ShipmentCreate
) -> ShipmentResponse:
    """
    Update a shipment record by ID.
    """
    result = await db.execute(
        select(ShipmentModel).filter(ShipmentModel.id == shipment_id)
    )
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found."
        )

    for key, value in shipment_in.model_dump(exclude_unset=True).items():
        setattr(shipment, key, value)

    db.add(shipment)
    await db.commit()
    await db.refresh(shipment)

    return ShipmentResponse.model_validate(shipment, from_attributes=True)


# 🔴 Delete a shipment
async def delete_shipment(db: AsyncSession, shipment_id: int) -> bool:
    """
    Delete a shipment record by its ID.
    """
    result = await db.execute(
        select(ShipmentModel).filter(ShipmentModel.id == shipment_id)
    )
    shipment = result.scalar_one_or_none()
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found."
        )

    await db.execute(delete(ShipmentModel).where(ShipmentModel.id == shipment_id))
    await db.commit()
    return True
