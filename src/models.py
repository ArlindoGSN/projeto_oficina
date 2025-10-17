from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import (
    Mapped,
    mapped_as_dataclass,
    mapped_column,
    registry,
    relationship,
)

from .security import hash_password, verify_password

# Registry do SQLAlchemy
mapper_registry = registry()


@mapped_as_dataclass(mapper_registry, kw_only=True)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    _password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relacionamento com File
    files: Mapped[List["File"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, plain_password: str) -> None:
        self._password = hash_password(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return verify_password(plain_password, self._password)

    def __init__(self, username: str, email: str, password: str, is_active: bool = True):
        self.username = username
        self.email = email
        self.password = password  # setter faz o hash
        self.is_active = is_active


@mapped_as_dataclass(mapper_registry, kw_only=True)
class File:
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # Relacionamento reverso com User
    user: Mapped["User"] = relationship(back_populates="files")
