from typing import Dict, Any

from sqlalchemy import select, insert, delete, update

from sqlalchemy.ext.asyncio import AsyncSession

from product import models, schemas


async def get_all_products(db: AsyncSession):
    query = select(models.DBProduct)
    product_list = await db.execute(query)

    return [product[0] for product in product_list.fetchall()]


async def get_single_product(db: AsyncSession, product_id: int):
    query = select(models.DBProduct).where(models.DBProduct.id == product_id)
    result = await db.execute(query)
    product = result.fetchone()

    if product is None:
        return None

    return product[0]


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    query = insert(models.DBProduct).values(
        name=product.name,
        type=product.type,
        daily_fee=product.daily_fee,
        inventory=product.inventory
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**product.model_dump(), "id": result.lastrowid}
    return resp


async def update_product(
    db: AsyncSession, product_id: int, product: schemas.ProductCreate
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
    result = await db.execute(query)
    await db.commit()

    if result.rowcount > 0:
        updated_product = {
            "id": product_id,
            **product.model_dump(),
        }
        return updated_product
    else:
        return {}


async def delete_product(db: AsyncSession, product_id: int):
    query = delete(models.DBProduct).where(models.DBProduct.id == product_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0
