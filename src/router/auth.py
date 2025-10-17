from http import HTTPStatus
from src.schemas import Token
from sqlalchemy import select
from fastapi import APIRouter, HTTPException
from src.models import User
from src.router.annotated import T_OAuth2Form, T_Session
from src.security import create_access_token, verify_password


router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: T_OAuth2Form, session: T_Session):
    user = await session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Incorrect username or password"
        )

    access_token = create_access_token(data={"sub": user.username})

    return Token(access_token=access_token, token_type="bearer")
