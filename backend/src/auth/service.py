from datetime import timedelta, datetime, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.config import auth_settings
from src.auth.constants import TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.auth.exeptions import credentials_exception
from src.auth.utils import validate_token_type
from src.crud import get_user_by_id
from src.database import get_db
from src.models import User

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def encode_jwt(
        payload: dict,
        expire_minutes: int = auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, auth_settings.SECRET_KEY, algorithm=auth_settings.ALGORITHM)


def create_jwt(
        token_type: str,
        payload: dict,
        expire_minutes: int = auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta
    )


def create_access_token(user: User) -> str:
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        payload=jwt_payload,
        expire_minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub": str(user.id),
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        payload=jwt_payload,
        expire_timedelta=timedelta(days=auth_settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def get_current_token_payload(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, auth_settings.SECRET_KEY, algorithms=auth_settings.ALGORITHM)
    except JWTError:
        raise credentials_exception
    return payload


def get_auth_user_from_token_of_type(token_type: str):
    async def get_auth_user_from_token(
            payload: dict = Depends(get_current_token_payload),
            db: AsyncSession = Depends(get_db)
    ) -> User:
        validate_token_type(payload, token_type)
        return await get_user_by_token_sub(payload, db)

    return get_auth_user_from_token


async def get_user_by_token_sub(payload: dict, db: AsyncSession):
    id_user: int | None = int(payload.get("sub"))
    if user := await get_user_by_id(id_user, db):
        return user
    raise credentials_exception


get_current_user_for_refreash = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)
get_current_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
