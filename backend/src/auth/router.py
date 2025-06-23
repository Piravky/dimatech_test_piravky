from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth.config import password_manager
from src.auth.exeptions import invalid_auth_exception
from src.auth.schemas import Token
from src.auth.service import create_access_token, create_refresh_token, get_current_user_for_refreash
from src.database import get_db
from src.models import User

auth_router = APIRouter(
    tags=["auth"],
)


@auth_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)) -> Token:
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    if not user:
        raise invalid_auth_exception
    if not password_manager.verify_password(form_data.password, user.password):
        raise invalid_auth_exception

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.post("/refresh", response_model=Token)
async def refresh(user: User = Depends(get_current_user_for_refreash)) -> Token:
    access_token = create_access_token(user)
    return Token(
        access_token=access_token
    )
