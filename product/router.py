from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db
from product import crud, schemas


router = APIRouter()

PRODUCT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
)


@router.get("/products/", response_model=list[schemas.Product])
def read_product(db: Session = Depends(get_db)):
    return crud.get_all_products(db=db)


@router.get("/products/{product_id}", response_model=schemas.Product)
def read_single_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_single_product(db=db, product_id=product_id)
    if product is None:
        raise PRODUCT_NOT_FOUND
    return product


@router.post("/products/", response_model=schemas.ProductCreate)
def create_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    return crud.create_product(db=db, product=product)


@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.update_product(db=db, product_id=product_id, product=product)


@router.delete("/products/{product_id}", response_model=schemas.ProductDelete)
def delete_product(
    product_id: int, db: Session = Depends(get_db)
):
    deleted = crud.delete_product(db=db, product_id=product_id)
    if not deleted:
        raise PRODUCT_NOT_FOUND
    return {"id": product_id}
