from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.service import get_current_user
from src.config import settings
from src.crud import (
    get_accounts,
    get_transactions,
    get_users,
    get_user_by_email,
    get_user_by_id,
    add_user,
    update_user,
    delete_user_by_id,
    add_transaction,
    increase_amount,
    create_account,
    get_account_by_id_filtered_user_id
)
from src.database import get_db
from src.models import UserRole
from src.users.exeptions import dont_have_permission, email_is_registered, invalid_signature
from src.users.schemas import (
    Transaction,
    UserBase,
    UserCreate,
    UserUpdate,
    UserPublic,
    UserPublicWithAccount,
    AccountPublic,
    TransactionPublic
)
from src.users.utils import verify_signature

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/", response_model=List[UserPublicWithAccount])
async def get_user(current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise dont_have_permission

    return await get_users(db)


@user_router.post("/", response_model=UserPublic)
async def create_user(user: UserCreate, current_user: UserBase = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise dont_have_permission
    exists_user = await get_user_by_email(user.email, db)
    if exists_user:
        raise email_is_registered

    return await add_user(user, db)


@user_router.patch("/{user_id}", response_model=UserPublic)
async def update_user(user_id: int, user: UserUpdate, current_user: UserBase = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise dont_have_permission
    exists_user = await get_user_by_id(user_id, db)
    if exists_user:
        raise email_is_registered  # FIXME: replace this HTTPEXEPTION
    return await update_user(user_id, user, db)


@user_router.delete("/{user_id}")
async def delete_user(user_id: int, current_user: UserBase = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise dont_have_permission
    if await delete_user_by_id(user_id, db):
        return {"message": "OK"}
    raise {"message": "User not found"}


@user_router.get("/me", response_model=UserPublic)
async def get_me(current_user: UserBase = Depends(get_current_user)):
    return current_user


@user_router.get("/account", response_model=List[AccountPublic])
async def get_account(current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    accounts = await get_accounts(current_user.id, db)
    return accounts


@user_router.get("/transaction", response_model=List[TransactionPublic])
async def get_transaction(current_user: UserBase = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    transactions = await get_transactions(current_user.id, db)
    return transactions


@user_router.post("/transaction")
async def create_transaction(transaction: Transaction, db: AsyncSession = Depends(get_db)):
    message = f"{transaction.account_id}{transaction.amount}{transaction.transaction_id}{transaction.user_id}{settings.SIGNATURE_SIGN}"
    if not verify_signature(message, transaction.signature):
        raise invalid_signature
    exists_account = await get_account_by_id_filtered_user_id(transaction.user_id, transaction.account_id, db)
    if not exists_account:
        await create_account(transaction.user_id, transaction.account_id, db)
    if await add_transaction(transaction, db):
        await increase_amount(transaction.account_id, transaction.amount, db)
        return {"message": "OK"}

    return {"message": "error"}
