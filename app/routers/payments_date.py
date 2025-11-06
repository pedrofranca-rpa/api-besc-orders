from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.payments import create_payment, get_payment_by_order_code
from app.schemas.payments import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/api/payments-date", tags=["Payments Date"])


@router.post("/", response_model=PaymentResponse)
async def create_payment_date(
    payment: PaymentCreate, db: AsyncSession = Depends(get_db)
):
    return await create_payment(db, payment)


@router.get("/{id}", response_model=PaymentResponse)
async def get_payment_date(id: int, db: AsyncSession = Depends(get_db)):
    return await get_payment_by_order_code(db, id)
