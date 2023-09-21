from typing import Dict, Any

from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import Session

from product import models, schemas


def get_all_products(db: Session):
    query = select(models.DBProduct)
    cities_list = db.execute(query)

    return [city[0] for city in cities_list.fetchall()]


def get_single_product(db: Session, product_id: int):
    query = select(models.DBProduct).where(models.DBProduct.id == product_id)
    result = db.execute(query)
    product = result.fetchone()

    if product is None:
        return None

    return product[0]


def create_product(db: Session, product: schemas.ProductCreate):
    query = insert(models.DBProduct).values(
        name=product.name, type=product.type, daily_fee=product.daily_fee
    )
    result = db.execute(query)
    db.commit()
    resp = {**product.model_dump(), "id": result.lastrowid}
    return resp


def update_product(
    db: Session, product_id: int, product: schemas.ProductCreate
) -> Dict[str, Any]:
    query = (
        update(models.DBProduct)
        .where(models.DBProduct.id == product_id)
        .values(
            name=product.name,
            type=product.type,
            daily_fee=product.daily_fee
        )
    )
    result = db.execute(query)
    db.commit()

    if result.rowcount > 0:
        updated_product = {
            "id": product_id,
            **product.model_dump(),
        }
        return updated_product
    else:
        return {}


def delete_product(db: Session, product_id: int):
    query = delete(models.DBProduct).where(models.DBProduct.id == product_id)
    result = db.execute(query)
    db.commit()
    return result.rowcount > 0
