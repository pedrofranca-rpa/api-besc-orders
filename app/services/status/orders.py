from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.orders import Order as OrderModel
from app.schemas.orders import OrderCreate


# 🟠 Update order
async def update_order_status(db: AsyncSession, order_id: int, data: OrderCreate):
    try:
        result = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
        order = result.scalars().first()

        if not order:
            return JSONResponse(status_code=404, content={"message": "Order not found"})

        order.status_id = data.status_id

        db.add(order)
        await db.commit()
        await db.refresh(order)

        return JSONResponse(
            status_code=200,
            content={
                "message": "Order updated successfully!",
                "order": order_id,
                "status": data.status_id,
            },
        )

    except IntegrityError as e:
        await db.rollback()
        return JSONResponse(
            status_code=400,
            content={
                "message": "Database integrity error",
                "error": str(e.orig),
            },
        )
    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "Internal error while updating order", "error": str(e)},
        )
