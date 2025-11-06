from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.payments import Payment as PaymentModel
from app.schemas.payments import PaymentCreate, PaymentResponse
from app.models.orders import Order as OrderModel


# 🟢 Create a payment
async def create_payment(
    db: AsyncSession, payment_in: PaymentCreate
) -> PaymentResponse:
    """
    Create a new payment record.
    """
    db_payment = PaymentModel(**payment_in.model_dump())
    db.add(db_payment)

    try:
        await db.commit()
        await db.refresh(db_payment)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create payment: {str(e)}",
        )

    return PaymentResponse.model_validate(db_payment, from_attributes=True)


async def get_payment_by_order_code(
    db: AsyncSession, order_code: int
) -> PaymentResponse:
    """
    Retrieve a payment record by the BESC order code.
    """

    # Step 1️⃣ — Find the order by its BESC order code
    result_order = await db.execute(
        select(OrderModel).where(OrderModel.vale_order_id == order_code)
    )
    order = result_order.scalar_one_or_none()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with code {order_code} not found.",
        )

    # Step 2️⃣ — Retrieve the payment linked to that order
    result_payment = await db.execute(
        select(PaymentModel).where(PaymentModel.id == order.payment_id)
    )
    payment = result_payment.scalar_one_or_none()

    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No payment record found for order code {order_code}.",
        )

    # Step 3️⃣ — Return validated Pydantic response
    return PaymentResponse.model_validate(payment, from_attributes=True)
