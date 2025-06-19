from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import User

async def get_user(user_id: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()