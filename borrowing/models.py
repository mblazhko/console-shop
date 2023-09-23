from sqlalchemy import Column, Integer, DateTime, func, Boolean
from database import Base


class DBBorrowing(Base):
    __tablename__ = "borrowing"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )
    product_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    borrow_date = Column(DateTime, server_default=func.now(), nullable=False)
    expected_return_date = Column(DateTime, nullable=False)
    actual_return_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=True, default=True)
