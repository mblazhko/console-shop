from fastapi import HTTPException
from sqlalchemy import select, insert, func
from sqlalchemy.orm import Session

from borrowing import models, schemas
from product import models as product_models


def get_all_borrowings(db: Session):
    query = select(models.DBBorrowing)
    borrowing_list = db.execute(query)

    return [borrowing[0] for borrowing in borrowing_list.fetchall()]


def get_single_borrowing(db: Session, borrowing_id: int):
    query = select(models.DBBorrowing).where(models.DBBorrowing.id == borrowing_id)
    result = db.execute(query)
    borrowing = result.fetchone()

    if borrowing is None:
        return None

    return borrowing[0]


def create_borrowing(db: Session, borrowing: schemas.BorrowingCreate):
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
        result = db.execute(query)
        product.inventory -= 1
        db.commit()
        resp = {**borrowing.model_dump(), "id": result.lastrowid}
        return resp
    else:
        raise HTTPException(status_code=404, detail="Product not found")


def return_borrowing(db: Session, borrowing_id: int):
    borrowing = db.query(models.DBBorrowing).filter(
        models.DBBorrowing.id == borrowing_id
    ).first()
    if borrowing.is_active:
        borrowing.is_active = False
        borrowing.actual_return_date = func.now()
        db.commit()
        return {"message": "Borrowing is successfully returned"}
    else:
        return {"message": "Borrowing is already returned"}
