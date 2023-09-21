from pydantic import BaseModel
from enum import Enum


class ProductType(str, Enum):
    console = "console"
    game = "game"


class ProductBase(BaseModel):
    name: str
    type: ProductType
    daily_fee: float


class ProductCreate(ProductBase):
    pass


class ProductDelete(BaseModel):
    id: int


class Product(ProductBase):
    id: int