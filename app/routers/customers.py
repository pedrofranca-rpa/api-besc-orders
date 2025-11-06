from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.customers import (
    create_customer,
    get_customer,
    get_all_customers,
    update_customer,
    delete_customer,
)
from app.schemas.customers import Customer, CustomerCreate

router = APIRouter(prefix="/api/customers", tags=["Customers"])


# 🟢 Create a new customer
@router.post("/", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer_route(
    customer: CustomerCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new customer.
    """
    return await create_customer(db, customer)


# 🔵 Get a customer by ID
@router.get("/{id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def get_customer_route(id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a customer by its ID.
    """
    return await get_customer(db, id)


# 🟣 List all customers
@router.get("/", response_model=list[Customer], status_code=status.HTTP_200_OK)
async def list_customers(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip."),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of records to return."
    ),
):
    """
    Retrieve all customers with pagination.
    """
    return await get_all_customers(db, skip, limit)


# 🟠 Update a customer
@router.put("/{id}", response_model=Customer, status_code=status.HTTP_200_OK)
async def update_customer_route(
    id: int, customer: CustomerCreate, db: AsyncSession = Depends(get_db)
):
    """
    Update a customer's information.
    """
    return await update_customer(db, id, customer)


# 🔴 Delete a customer
@router.delete("/{id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_customer_route(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a customer by ID.
    """
    return await delete_customer(db, id)
