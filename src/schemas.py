from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserDetails(UserCreate):
    id: int
    is_active: bool


class UserPatch(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None

class UserLogin(BaseModel):
    username: str
    password: str


class ItemDetails(BaseModel):
    id: int
    filename: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
