import decimal

from pydantic import BaseModel, condecimal, field_validator
from enum import Enum


class ProductType(str, Enum):
    console = "console"
    game = "game"


class ProductBase(BaseModel):
    name: str
    type: ProductType
    daily_fee: condecimal(ge=decimal.Decimal('0.00'), max_digits=10, decimal_places=2)
    inventory: int

    @field_validator("inventory")
    @classmethod
    def validate_inventory(cls, values):
        if values is not None and values < 0:
            raise ValueError("Inventory must be a non-negative integer")
        return values


class ProductCreate(ProductBase):
    pass


class ProductDelete(BaseModel):
    id: int


class Product(ProductBase):
    id: int