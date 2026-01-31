from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from db.models import User
from dotenv import load_dotenv
import os




load_dotenv("C:/Users/Asus/Desktop/aiogram/shop-bot/bot_long_messages.env")

bot_message1 = os.getenv("MESSAGE1")

# start_handler handler service
async def register(message: Message, db: AsyncSession, telegram_id: int):
    user = await User.get_full_record_by_telegram_id(telegram_id)
    if not user:
        username = message.from_user.username or f"user_{telegram_id}"
        first_name = message.from_user.first_name or ""
        last_name = message.from_user.last_name or ""
        user = await User.create_user(
            telegram_id=telegram_id,
            language_code=message.from_user.language_code,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

    bot_answer = bot_message1
    return bot_answer


