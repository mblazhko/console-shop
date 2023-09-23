from fastapi import HTTPException
from sqlalchemy import select, insert, func
from sqlalchemy.ext.asyncio import AsyncSession
from borrowing import models, schemas
from product import models as product_models


async def get_all_borrowings(db: AsyncSession, user_id: int, is_active: bool = None):
    query = select(models.DBBorrowing).where(
        models.DBBorrowing.user_id == user_id
    )
    borrowing_list = await db.execute(query)

    return [borrowing[0] for borrowing in borrowing_list.fetchall()]


async def get_single_borrowing(db: AsyncSession, borrowing_id: int):
    query = select(models.DBBorrowing).where(models.DBBorrowing.id == borrowing_id)
    result = await db.execute(query)
    borrowing = result.fetchone()

    if borrowing is None:
        return None

    return borrowing[0]


async def create_borrowing(db: AsyncSession, borrowing: schemas.BorrowingCreate):
    product = db.query(product_models.DBProduct).filter(
        product_models.DBProduct.id == borrowing.product_id
    ).first()

    if product is not None:
        if product.inventory == 0:
            raise HTTPException(
                status_code=400,
                detail="Inventory for this product is currently zero. Cannot make borrowing."
            )

        query = insert(models.DBBorrowing).values(
            product_id=borrowing.product_id,
            user_id=borrowing.user_id,
            borrow_date=borrowing.borrow_date,
            expected_return_date=borrowing.expected_return_date,
            actual_return_date=borrowing.actual_return_date,
            is_active=borrowing.is_active
        )
        result = await db.execute(query)
        product.inventory -= 1
        await db.commit()
        resp = {**borrowing.model_dump(), "id": result.lastrowid}
        return resp
    else:
        raise HTTPException(status_code=404, detail="Product not found")


async def return_borrowing(db: AsyncSession, borrowing_id: int):
    borrowing = db.query(models.DBBorrowing).filter(
        models.DBBorrowing.id == borrowing_id
    ).first()
    if borrowing.is_active:
        borrowing.is_active = False
        borrowing.actual_return_date = func.now()
        await db.commit()
        return {"message": "Borrowing is successfully returned"}
    else:
        return {"message": "Borrowing is already returned"}
