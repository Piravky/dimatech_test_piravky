from src.auth.constants import TOKEN_TYPE_FIELD
from src.auth.exeptions import credentials_exception


def validate_token_type(payload: dict, token_type: str) -> bool:
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise credentials_exception
