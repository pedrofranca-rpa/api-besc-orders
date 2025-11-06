from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from fastapi import HTTPException, status

from app.models.customers import Customer as CustomerModel
from app.schemas.customers import CustomerCreate, Customer


# =====================================================================
# 1️⃣ CREATE CUSTOMER
# =====================================================================
async def create_customer(db: AsyncSession, customer_in: CustomerCreate) -> Customer:
    """
    Create a new customer.

    Args:
        db: Async database session.
        customer_in: Input data for the customer (name).

    Returns:
        Customer: Created customer object with its ID.
    """
    # Check if a customer with the same name already exists
    result = await db.execute(
        select(CustomerModel).filter(CustomerModel.name == customer_in.name)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A customer with this name already exists.",
        )

    db_customer = CustomerModel(**customer_in.model_dump())
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return Customer.model_validate(db_customer, from_attributes=True)


# =====================================================================
# 2️⃣ GET CUSTOMER BY ID
# =====================================================================
async def get_customer(db: AsyncSession, customer_id: int) -> Customer:
    """
    Retrieve a customer by its ID.

    Raises:
        HTTPException 404: If customer is not found.
    """
    result = await db.execute(
        select(CustomerModel).filter(CustomerModel.id == customer_id)
    )
    customer = result.scalar_one_or_none()

    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found."
        )

    return Customer.model_validate(customer, from_attributes=True)


# =====================================================================
# 3️⃣ LIST ALL CUSTOMERS
# =====================================================================
async def get_all_customers(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> list[Customer]:
    """
    Retrieve a paginated list of customers.
    """
    result = await db.execute(
        select(CustomerModel).offset(skip).limit(limit).order_by(CustomerModel.id)
    )
    customers = result.scalars().all()
    return [Customer.model_validate(c, from_attributes=True) for c in customers]


# =====================================================================
# 4️⃣ UPDATE CUSTOMER
# =====================================================================
async def update_customer(
    db: AsyncSession, customer_id: int, customer_in: CustomerCreate
) -> Customer:
    """
    Update a customer's name.
    """
    await db.execute(
        update(CustomerModel)
        .where(CustomerModel.id == customer_id)
        .values(name=customer_in.name)
    )
    await db.commit()
    return await get_customer(db, customer_id)


# =====================================================================
# 5️⃣ DELETE CUSTOMER
# =====================================================================
async def delete_customer(db: AsyncSession, customer_id: int) -> dict:
    """
    Delete a customer.
    ⚠️ Warning: This may fail if there are linked orders (FK constraint).
    """
    await db.execute(delete(CustomerModel).where(CustomerModel.id == customer_id))
    await db.commit()
    return {"detail": "Customer successfully deleted."}
