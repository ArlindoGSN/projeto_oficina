from fastapi import FastAPI, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from .database import get_db
from .schemas import Message, TokenResponse, UserCreate, UserDetails, UserLogin
from .services import create_user, login_user

app = FastAPI()


@app.get("/health", response_model=Message, status_code=status.HTTP_200_OK)
def read_health():
    return Message(message="OK")


@app.post("/register", response_model=UserDetails, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)


@app.post("/login", response_model=TokenResponse, status_code=status.HTTP_202_ACCEPTED)
def login(request: UserLogin, db: Session = Depends(get_db)):
    return login_user(request, db)
