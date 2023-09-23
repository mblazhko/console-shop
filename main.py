from fastapi import FastAPI, Depends
from product import router as product_router
from borrowing import router as borrowing_router

app = FastAPI()

app.include_router(product_router.router)
app.include_router(borrowing_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to ConsoleShop"}
