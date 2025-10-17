from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from src.models import User
from src.schemas import UserCreate, UserPatch, UserDetails

from src.router.annotated import T_Session, T_User
from src.security import get_password_hash


router = APIRouter()


@router.post("/", response_model=UserDetails)
async def create_user(user: UserCreate, session: T_Session):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password)
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.get("/", response_model=UserDetails)
async def get_user(session: T_Session, current_user: T_User):
    db_user = await session.scalar(select(User).where(User.id == current_user.id))

    return db_user


@router.patch("/", response_model=UserDetails)
async def patch_user(user: UserPatch, session: T_Session, current_user: T_User):
    db_user = await session.scalar(
        select(User).where(
            ((User.username == user.username) | (User.email == user.email))
            & (User.id != current_user.id)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username already exists",
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Email already exists",
            )

    db_user = await session.scalar(select(User).where(User.id == current_user.id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")

    for key, value in user.model_dump(exclude_unset=True).items():
        if key == "password":
            value = get_password_hash(value)
        setattr(db_user, key, value)

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


@router.delete("/")
async def delete_user(session: T_Session, current_user: T_User):
    db_user = await session.scalar(select(User).where(User.id == current_user.id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    await session.delete(db_user)
    await session.commit()

    return {"User deleted"}
