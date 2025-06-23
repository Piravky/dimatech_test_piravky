from pydantic import EmailStr
from pydantic.v1 import UUID4
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.auth.config import password_manager
from src.models import User, Account, Transaction


async def get_users(db: AsyncSession):
    result = await db.execute(select(User).options(selectinload(User.accounts)))
    users = result.scalars().all()
    return users


async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(email: EmailStr, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def add_user(user, db: AsyncSession):
    new_user = User(
        email=user.email,
        password=password_manager.get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user(user_id: int, user_updata, db: AsyncSession):
    user = await get_user_by_id(user_id, db)

    update_data = user_updata.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "password":
            value = password_manager.get_password_hash(value)
        elif key == "email":
            existing_email = await get_user_by_email(user.email, db)
            if existing_email:
                return None  # FIXME: maybe replace this
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_by_id(user_id: int, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not user:
        return None
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()
    return "OK"  # FIXME: Пересмотреть логику


async def get_accounts(user_id: int, db: AsyncSession):
    result = await db.execute(select(Account).filter(Account.user_id == user_id))
    return result.scalars().all()


async def get_account_by_id(account_id: int, db: AsyncSession):
    result = await db.execute(select(Account).filter(Account.id == account_id))
    return result.scalars().first()


async def increase_amount(account_id: int, amount: int, db: AsyncSession):
    account = await get_account_by_id(account_id, db)
    new_balance = account.balance + amount
    setattr(account, "balance", new_balance)
    await db.commit()
    await db.refresh(account)
    return account


async def create_account(user_id: int, account_id: int, db: AsyncSession):
    new_account = Account(
        id=account_id,
        user_id=user_id,
        balance=0
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account


async def get_account_by_id_filtered_user_id(user_id: int, account_id: int, db: AsyncSession):
    result = await db.execute(select(Account).filter(Account.id == account_id, Account.user_id == user_id))
    return result.scalars().first()


async def add_transaction(transaction, db: AsyncSession):
    exists_transaction = await get_transactions_by_id(transaction.transaction_id, db)
    if exists_transaction:
        return None
    new_transaction = Transaction(
        id=transaction.transaction_id,
        account_id=transaction.account_id,
        amount=transaction.amount,
        user_id=transaction.user_id,
    )
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction


async def get_transactions(user_id: int, db: AsyncSession):
    result = await db.execute(select(Transaction).filter(Transaction.user_id == user_id))
    return result.scalars().all()


async def get_transactions_by_id(transaction_id: UUID4, db: AsyncSession):
    result = await db.execute(select(Transaction).filter(Transaction.id == transaction_id))
    return result.scalars().first()
