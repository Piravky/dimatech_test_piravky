from pydantic import BaseModel, UUID4, EmailStr

from src.models import UserRole


class AccountBase(BaseModel):
    pass


class AccountPublic(AccountBase):
    id: int
    balance: float


class Transaction(BaseModel):
    transaction_id: UUID4
    user_id: int
    account_id: int
    amount: int
    signature: str


class TransactionPublic(BaseModel):
    id: UUID4
    account_id: int
    amount: float
    user_id: int


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole


class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    role: UserRole | None = None


class UserPublic(UserBase):
    email: EmailStr
    full_name: str


class UserPublicWithAccount(UserBase):
    email: EmailStr
    full_name: str
    accounts: list[AccountPublic] = []
