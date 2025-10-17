from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import User
from .schemas import TokenResponse, UserCreate, UserDetails, UserLogin
from .security import create_access_token, verify_password


def create_user(user: UserCreate, db: Session) -> UserDetails:
    # verifica se já existe usuário com mesmo email ou username
    existing_user = (
        db.query(User).filter((User.email == user.email) | (User.username == user.username)).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already registered"
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return UserDetails.model_validate(db_user)


def login_user(login: UserLogin, db: Session):
    user: User = db.query(User).filter(User.email == login.email).first()
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=access_token, token_type="bearer")
