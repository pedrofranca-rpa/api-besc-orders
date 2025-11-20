from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    customer_id = Column(
        Integer,
        ForeignKey("customers.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    payment_id = Column(
        Integer,
        ForeignKey("payments.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    status_id = Column(
        Integer,
        ForeignKey("orders_status.id", onupdate="CASCADE", ondelete="RESTRICT"),
        default=0,
    )
    state = Column(String(3))
    vale_order_id = Column(BigInteger, unique=True, nullable=False)
    total_value = Column(Numeric(12, 2), nullable=False)

    # Relationships

    portal = Column(String(50))
    center = Column(String(100))
    besc_order_id = Column(BigInteger, unique=True, nullable=True)
    contract_number = Column(String(100))
    invoice_number = Column(String(50))
    total_value = Column(Numeric(12, 2), nullable=False)

    proposal_id = Column(
        Integer,
        ForeignKey("proposals.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )

    payment = relationship("Payment", foreign_keys=[payment_id])

    # Relacionamento com Proposal
    proposals = relationship("Proposal", back_populates="order")

    # Relationships
    customer = relationship("Customer", back_populates="orders")

    status = relationship("OrdersStatus", back_populates="orders")

    # 🔹 1:1 com Shipment
    shipment = relationship(
        "Shipment",
        back_populates="order",
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )

    products = relationship(
        "Product", back_populates="order", cascade="all, delete-orphan"
    )
    tickets = relationship(
        "Ticket", back_populates="order", cascade="all, delete-orphan"
    )
