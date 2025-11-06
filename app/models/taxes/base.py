from sqlalchemy import Column, Numeric


class TaxBase:

    value = Column(Numeric(10, 2))
    rate = Column(Numeric(5, 2))
    base_amount = Column(Numeric(10, 2))
