from datetime import datetime
from sqlalchemy import String, ForeignKey, Integer, DateTime, Boolean, func, registry
from sqlalchemy.orm import Mapped, mapped_column, relationship, mapped_as_dataclass

mapper_registry = registry()


@mapped_as_dataclass(mapper_registry)
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), init=False
    )

    files: Mapped[list["File"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


@mapped_as_dataclass(mapper_registry)
class File:
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    filepath: Mapped[str] = mapped_column(String(500), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), init=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="files")

