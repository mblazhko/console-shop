from sqlalchemy import Column, Integer, String, Numeric
from database import Base


class DBProduct(Base):
    __tablename__ = "product"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    name = Column(String(255), nullable=False)
    type = Column(String(511), nullable=False)
    daily_fee = Column(Numeric(precision=10, scale=2), nullable=False)
    inventory = Column(Integer, nullable=False)
