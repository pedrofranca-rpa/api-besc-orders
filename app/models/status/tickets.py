from app.models.status.base import BaseStatus
from sqlalchemy.orm import relationship


class TicketStatus(BaseStatus):
    __tablename__ = "tickets_status"
    tickets = relationship("Ticket", back_populates="status")
