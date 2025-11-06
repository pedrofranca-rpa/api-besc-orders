from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Customer(Base):
    __tablename__ = "customers"

    name = Column(String(255), nullable=False)
    tax_id = Column(String(20))  # CNPJ/CPF equivalent

    # Relationships
    orders = relationship(
        "Order", back_populates="customer", cascade="all, delete-orphan"
    )
