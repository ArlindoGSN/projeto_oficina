from pydantic import BaseModel


class UserDetails(BaseModel):
    id: int
    username: str
    email: str
    password: str
    is_active: bool


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class ItemDetails(BaseModel):
    id: int
    name: str
    description: str | None = None
