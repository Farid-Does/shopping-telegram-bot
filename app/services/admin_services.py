# admin handlers services

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User




# register_admin handler service
async def check_admin(message: Message, db: AsyncSession, telegram_id: int, admins: list[int]):
    if telegram_id in admins:
        user = await User.get_full_record_by_telegram_id(db, telegram_id)
        user.is_admin = True
        bot_answer = "successfully saved as an admin."
    else:
        bot_answer = "unfortunately, your ID was not found in the admin ID list."
    return bot_answer