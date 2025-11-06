from app.db.base import Base
from sqlalchemy.orm import relationship

from app.models.taxes.base import TaxBase


class ICMS(TaxBase, Base):
    __tablename__ = "icms"
    # Relationship
    tax = relationship("Tax", back_populates="icms", uselist=False)
