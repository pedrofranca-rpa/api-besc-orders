from app.db.base import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Tax(Base):
    __tablename__ = "tax"

    icms_id = Column(
        Integer, ForeignKey("icms.id", onupdate="CASCADE", ondelete="SET NULL")
    )
    ipi_id = Column(
        Integer, ForeignKey("ipi.id", onupdate="CASCADE", ondelete="SET NULL")
    )

    # Relationships
    icms = relationship("ICMS", back_populates="tax")
    ipi = relationship("IPI", back_populates="tax")
    products = relationship("Product", back_populates="tax")
