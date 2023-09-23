from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from dependencies import get_db
from borrowing import crud, schemas


router = APIRouter()

BORROWING_NOT_FOUND = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing not found"
)


@router.get("/borrowings/", response_model=list[schemas.Borrowing])
def read_product(db: Session = Depends(get_db)):
    return crud.get_all_borrowings(db=db)


@router.get("/borrowings/{borrowing_id}", response_model=schemas.Borrowing)
def read_single_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    borrowing = crud.get_single_borrowing(borrowing_id=borrowing_id, db=db)
    if borrowing is None:
        return BORROWING_NOT_FOUND
    return borrowing


@router.post("/borrowings/", response_model=schemas.BorrowingCreate)
def create_borrowing(
        borrowing: schemas.BorrowingCreate,
        db: Session = Depends(get_db)
):
    return crud.create_borrowing(borrowing=borrowing, db=db)


@router.get("/borrowings/{borrowing_id}/return-borrowing", response_model=schemas.Borrowing)
def return_borrowing(borrowing_id: int, db: Session = Depends(get_db)):
    return crud.return_borrowing(borrowing_id=borrowing_id, db=db)



