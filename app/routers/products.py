from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.products import ProductResponse, ProductCreate
from app.services.products import (
    create_product,
    get_product,
    get_products_by_order,
)

router = APIRouter(prefix="/api/products", tags=["Products"])


# 🔵 Get product by ID
@router.get("/{id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product_by_id(id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve a single product by its ID.
    """
    return await get_product(db, id)


# 🟣 Get all products for a specific order
@router.get(
    "/order/{order_id}",
    response_model=List[ProductResponse],
    status_code=status.HTTP_200_OK,
)
async def get_products_for_order(order_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all products linked to a given order.
    """
    return await get_products_by_order(db, order_id)


# 🟢 Bulk create products for an order
@router.post(
    "/bulk/order/{order_id}",
    response_model=List[ProductResponse],
    status_code=status.HTTP_201_CREATED,
)
async def create_products_bulk(
    order_id: int, products: List[ProductCreate], db: AsyncSession = Depends(get_db)
):
    """
    Create multiple products linked to the same order.
    """
    created = []
    for prod in products:
        prod.order_id = order_id  # Link the order
        product_created = await create_product(db, prod)
        created.append(product_created)
    return created
