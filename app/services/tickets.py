from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException, status

from app.models.tickets import Ticket as TicketModel
from app.schemas.tickets import TicketCreate, TicketResponse


# 🟢 Create a ticket
async def create_ticket(db: AsyncSession, ticket_in: TicketCreate) -> TicketResponse:
    """
    Create a new support ticket.
    """
    db_ticket = TicketModel(**ticket_in.model_dump())
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return TicketResponse.model_validate(db_ticket, from_attributes=True)


# 🔵 Get ticket by ID
async def get_ticket(db: AsyncSession, ticket_id: int) -> TicketResponse:
    """
    Retrieve a single ticket by its ID.
    """
    result = await db.execute(select(TicketModel).where(TicketModel.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    return TicketResponse.model_validate(ticket, from_attributes=True)


# 🟠 Update a ticket
async def update_ticket(
    db: AsyncSession, ticket_id: int, ticket_in: TicketCreate
) -> TicketResponse:
    """
    Update an existing ticket by its ID.
    """
    result = await db.execute(select(TicketModel).where(TicketModel.id == ticket_id))
    existing_ticket = result.scalar_one_or_none()

    if not existing_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    await db.execute(
        update(TicketModel)
        .where(TicketModel.id == ticket_id)
        .values(**ticket_in.model_dump(exclude_unset=True))
    )

    await db.commit()
    return await get_ticket(db, ticket_id)


# 🔴 Delete a ticket
async def delete_ticket(db: AsyncSession, ticket_id: int):
    """
    Delete a ticket by its ID.
    """
    result = await db.execute(select(TicketModel).where(TicketModel.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )

    await db.execute(delete(TicketModel).where(TicketModel.id == ticket_id))
    await db.commit()
    return {"message": "Ticket successfully deleted"}
