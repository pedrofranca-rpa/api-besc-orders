from sqlalchemy import Column, Integer, Date
from app.db.base import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    payment_date = Column(Date)
    billing_until = Column(Date)
