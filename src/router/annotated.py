from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_session
from src.security import get_current_user


T_Session = Annotated[AsyncSession, Depends(get_session)]
T_User = Annotated[str, Depends(get_current_user)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
