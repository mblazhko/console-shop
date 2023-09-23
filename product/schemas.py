import decimal

from pydantic import BaseModel, PositiveInt
from enum import Enum


class ProductType(str, Enum):
    console = "console"
    game = "game"


class ProductBase(BaseModel):
    name: str
    type: ProductType
    daily_fee: decimal.Decimal
    inventory: PositiveInt


class ProductCreate(ProductBase):
    pass


class ProductDelete(BaseModel):
    id: int


class Product(ProductBase):
    id: int