from pydantic import BaseModel


class Message(BaseModel):
    message: str


class UserDetails(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    model_config = {"from_attributes": True}  # permite criar a partir de instâncias ORM


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
    email: str
    password: str


class ItemDetails(BaseModel):
    id: int
    name: str
    description: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
