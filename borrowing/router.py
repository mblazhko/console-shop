from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from borrowing import crud, schemas


router = APIRouter()

BORROWING_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing not found"
)


@router.get("/borrowings/", response_model=list[schemas.Borrowing])
async def read_product(user_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_all_borrowings(db=db, user_id=user_id)


@router.get("/borrowings/{borrowing_id}", response_model=schemas.Borrowing)
async def read_single_borrowing(borrowing_id: int, db: AsyncSession = Depends(get_db)):
    borrowing = await crud.get_single_borrowing(borrowing_id=borrowing_id, db=db)
    if borrowing is None:
        return BORROWING_NOT_FOUND
    return borrowing


@router.post("/borrowings/", response_model=schemas.BorrowingCreate)
async def create_borrowing(
        borrowing: schemas.BorrowingCreate,
        db: AsyncSession = Depends(get_db)
):
    return await crud.create_borrowing(borrowing=borrowing, db=db)


@router.get("/borrowings/{borrowing_id}/return-borrowing", response_model=schemas.Borrowing)
async def return_borrowing(borrowing_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.return_borrowing(borrowing_id=borrowing_id, db=db)



