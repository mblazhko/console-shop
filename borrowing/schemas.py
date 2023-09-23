import datetime

from pydantic import BaseModel


class BorrowingBase(BaseModel):
    product_id: int
    payment_id: int
    user_id: int
    borrow_date: datetime.datetime
    expected_return_date: datetime.datetime
    actual_return_date: datetime.datetime
    is_active: bool


