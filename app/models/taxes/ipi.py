from app.db.base import Base
from sqlalchemy.orm import relationship

from app.models.taxes.base import TaxBase


class IPI(TaxBase, Base):
    __tablename__ = "ipi"
    # Relationship
    tax = relationship("Tax", back_populates="ipi", uselist=False)
