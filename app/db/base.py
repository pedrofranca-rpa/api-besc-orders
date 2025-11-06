from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, DateTime, func

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer


class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
