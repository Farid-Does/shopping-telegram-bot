from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from db.models import User
from dotenv import load_dotenv
import os




load_dotenv("C:/Users/Asus/Desktop/aiogram/shop-bot/bot_long_messages.env")

admin_start_message = os.getenv("ADMIN_START_MESSAGE")
bot_message1 = os.getenv("MESSAGE1")
admins = list(map(int, os.getenv("ADMINS").split(",")))

# start_handler handler service
async def register(
        message: Message,
        db: AsyncSession,
        telegram_id: int,
):
    user = await User.get_full_record_by_telegram_id(db, telegram_id)
    if not user:
        username = message.from_user.username or f"user_{telegram_id}"
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        user = await User.create_user(
            db,
            telegram_id=telegram_id,
            language_code=message.from_user.language_code,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

    if telegram_id in admins:
        user.is_admin = True
        bot_answer = admin_start_message
        return bot_answer
    else:
        bot_answer = bot_message1
        return bot_answer


