from fastapi import FastAPI, status
from src.router.user import router as user
from src.router.item import router as item
from src.router.auth import router as auth

app = FastAPI()

app.include_router(user, tags=['User'], prefix='/users')
app.include_router(item, tags=['Item'], prefix='/itens')
app.include_router(auth, tags=['Auth'], prefix='/auth')


@app.get("/", status_code=status.HTTP_200_OK)
async def read_root():
    return {'Hello, World'}


@app.get("/health", status_code=status.HTTP_200_OK)
async def read_health():
    return {'Ok'}
