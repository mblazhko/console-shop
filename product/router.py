from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from product import crud, schemas


router = APIRouter()

PRODUCT_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
)


@router.get("/products/", response_model=list[schemas.Product])
async def read_product(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_products(db=db)


@router.get("/products/{product_id}", response_model=schemas.Product)
async def read_single_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.get_single_product(db=db, product_id=product_id)
    if product is None:
        raise PRODUCT_NOT_FOUND
    return product


@router.post("/products/", response_model=schemas.ProductCreate)
async def create_product(
    product: schemas.ProductCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_product(db=db, product=product)


@router.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud.update_product(db=db, product_id=product_id, product=product)


@router.delete("/products/{product_id}", response_model=schemas.ProductDelete)
async def delete_product(
    product_id: int, db: AsyncSession = Depends(get_db)
):
    deleted = await crud.delete_product(db=db, product_id=product_id)
    if not deleted:
        raise PRODUCT_NOT_FOUND
    return {"id": product_id}
