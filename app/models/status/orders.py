# app/models/status/orders_status.py
from app.models.status.base import BaseStatus
from sqlalchemy.orm import relationship


class OrdersStatus(BaseStatus):
    __tablename__ = "orders_status"

    # Correto: o relacionamento é com a tabela de "orders"
    orders = relationship("Order", back_populates="status")
