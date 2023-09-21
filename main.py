from fastapi import FastAPI
from product import router as product_router

app = FastAPI()
app.include_router(product_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to ConsoleShop"}
