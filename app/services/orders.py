from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.orders import Order as OrderModel
from app.models.products import Product as ProductModel
from app.schemas.orders import OrderCreate, OrderWithProducts
from app.models.payments import Payment as PaymentModel


# 🟢 Create Order
async def create_order(db: AsyncSession, data: OrderCreate) -> JSONResponse:
    try:
        # 🟡 Check for duplicates
        result = await db.execute(
            select(OrderModel).where(OrderModel.vale_order_id == data.vale_order_id)
        )
        existing_order = result.scalar_one_or_none()
        if existing_order:
            return JSONResponse(
                status_code=400,
                content={
                    "message": f"An order with number {data.vale_order_id} already exists."
                },
            )

        result = await db.execute(
            select(PaymentModel).where(PaymentModel.id == data.payment_id)
        )
        existing_payment = result.scalar_one_or_none()
        if existing_payment:
            return JSONResponse(
                status_code=400,
                content={
                    "message": f"An payment with number {data.payment_id} already exists."
                },
            )

        # 🟢 Create the main order
        order = OrderModel(**data.model_dump(exclude={"products"}))
        db.add(order)
        await db.commit()
        await db.refresh(order)

        # ✅ Automatically convert decimals and datetimes
        order_data = jsonable_encoder(order)

        return JSONResponse(
            status_code=201,
            content={
                "message": "Order created successfully!",
                "order": order_data,
            },
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "Internal error while creating order", "error": str(e)},
        )


# 🔵 Get order with products
async def get_order_with_products(db: AsyncSession, order_number: int):
    result = await db.execute(
        select(OrderModel).where(OrderModel.vale_order_id == order_number)
    )
    order = result.scalars().first()

    if not order:
        return JSONResponse(status_code=404, content={"message": "Order not found"})

    # Get linked products
    result_prod = await db.execute(
        select(ProductModel).where(ProductModel.order_id == order.id)
    )
    products = result_prod.scalars().all()

    # Build response schema
    order_schema = OrderWithProducts.model_validate(
        {**order.__dict__, "products": products}, from_attributes=True
    ).model_dump()

    order_data = jsonable_encoder(order_schema)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Order found!",
            "order": order_data,
        },
    )


# 🟠 Update order
async def update_order(db: AsyncSession, order_id: int, data: OrderCreate):
    try:
        result = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
        order = result.scalars().first()

        if not order:
            return JSONResponse(status_code=404, content={"message": "Order not found"})

        # Update order fields
        for key, value in data.model_dump(
            exclude_unset=True, exclude={"products"}
        ).items():
            setattr(order, key, value)

        db.add(order)
        await db.commit()
        await db.refresh(order)

        # Update products (if provided)
        if data.products:
            # Remove existing products
            await db.execute(
                delete(ProductModel).where(ProductModel.order_id == order_id)
            )
            await db.commit()

            # Insert new products
            for p in data.products:
                product = ProductModel(**p.model_dump(), order_id=order.id)
                db.add(product)
            await db.commit()

        # Fetch updated products
        result_products = await db.execute(
            select(ProductModel).where(ProductModel.order_id == order.id)
        )
        products = result_products.scalars().all()

        return JSONResponse(
            status_code=200,
            content={
                "message": "Order updated successfully!",
                "order": OrderWithProducts.model_validate(
                    {**order.__dict__, "products": products},
                    from_attributes=True,
                ).model_dump(),
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


# 🔴 Delete order
async def delete_order(db: AsyncSession, order_id: int):
    try:
        result = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
        order = result.scalars().first()

        if not order:
            return JSONResponse(status_code=404, content={"message": "Order not found"})

        # Delete linked products first (FK)
        await db.execute(delete(ProductModel).where(ProductModel.order_id == order_id))
        await db.commit()

        # Delete the order itself
        await db.delete(order)
        await db.commit()

        return JSONResponse(
            status_code=200, content={"message": "Order deleted successfully!"}
        )

    except Exception as e:
        await db.rollback()
        return JSONResponse(
            status_code=500,
            content={"message": "Internal error while deleting order", "error": str(e)},
        )


# 🔵 Get single order
async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(
        select(OrderModel).where(OrderModel.vale_order_id == order_id)
    )
    order = result.scalars().first()

    if not order:
        return JSONResponse(status_code=404, content={"message": "Order not found"})

    # Fetch linked products
    result_products = await db.execute(
        select(ProductModel).where(ProductModel.order_id == order.id)
    )
    products = result_products.scalars().all()

    return JSONResponse(
        status_code=200,
        content={
            "message": "Order found!",
            "order": OrderWithProducts.model_validate(
                {**order.__dict__, "products": products}, from_attributes=True
            ).model_dump(),
        },
    )


# 🟣 Get all orders
async def get_all_orders(db: AsyncSession):
    result = await db.execute(select(OrderModel))
    orders = result.scalars().all()

    if not orders:
        return JSONResponse(status_code=404, content={"message": "No orders found"})

    orders_with_products = []

    for order in orders:
        result_prod = await db.execute(
            select(ProductModel).where(ProductModel.order_id == order.id)
        )
        products = result_prod.scalars().all()

        order_schema = OrderWithProducts.model_validate(
            {**order.__dict__, "products": products}, from_attributes=True
        ).model_dump()

        orders_with_products.append(order_schema)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Orders retrieved successfully!",
            "total": len(orders_with_products),
            "orders": orders_with_products,
        },
    )
