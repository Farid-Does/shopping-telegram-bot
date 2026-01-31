from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import AsyncSessionLocal


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        async with AsyncSessionLocal() as session:
            data["db"]: AsyncSession = session

            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise
