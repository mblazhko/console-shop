import datetime

from pydantic import BaseModel, field_validator


class BorrowingBase(BaseModel):
    product_id: int
    user_id: int
    borrow_date: datetime.datetime
    expected_return_date: datetime.datetime
    actual_return_date: datetime.datetime
    is_active: bool

    @field_validator("borrow_date", "expected_return_date")
    @classmethod
    def borrow_date_lte_expected_return_date(cls, values):
        if values["borrow_date"] > values["expected_return_date"]:
            raise ValueError(
                "Borrow date must be less than or equal to expected return date"
            )

    @field_validator("borrow_date", "actual_return_date")
    @classmethod
    def borrow_date_lte_actual_return_date(cls, values):
        if values["borrow_date"] > values["actual_return_date"]:
            raise ValueError(
                "Borrow date must be less than or equal to actual return date"
            )

    @field_validator("expected_return_date", "borrow_date")
    @classmethod
    def expected_return_date_gte_borrow_date(cls, values):
        if values["expected_return_date"] < values["borrow_date"]:
            raise ValueError(
                "Expected return date must be greater than or equal to borrow date"
            )

    @field_validator("actual_return_date", "borrow_date")
    @classmethod
    def actual_return_date_gte_borrow_date(cls, values):
        if values["actual_return_date"] < values["borrow_date"]:
            raise ValueError(
                "Actual return date must be greater than or equal to borrow date"
            )


class BorrowingCreate(BorrowingBase):
    pass


class Borrowing(BorrowingBase):
    id: int