from sqlalchemy import Column, Integer, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    order_id = Column(
        Integer,
        ForeignKey("orders.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    ticket_number = Column(Integer)
    opened_at = Column(Date)
    closed_at = Column(Date)
    status_id = Column(
        Integer,
        ForeignKey("tickets_status.id", onupdate="CASCADE", ondelete="SET NULL"),
    )
    notes = Column(Text)

    # Relationships
    order = relationship("Order", back_populates="tickets")
    status = relationship("TicketStatus", back_populates="tickets")
