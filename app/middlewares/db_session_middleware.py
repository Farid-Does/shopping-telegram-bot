# session middleware to inject sessions into handlers

from aiogram import BaseMiddleware
from db.database import async_session




# create db session middleware
class DbSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        async with async_session() as session:
            data["db"] = session

            try:
                result = await handler(event, data)
                await session.commit()
                return result
            except Exception:
                await session.rollback()
                raise