import os

from passlib.context import CryptContext
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), '../../.env'),
        env_prefix='AUTH_',
        extra='allow'
    )


auth_settings = AuthSettings()


class PasswordManager:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)


password_manager = PasswordManager()
