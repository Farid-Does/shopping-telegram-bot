from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message, ReplyKeyboardMarkup
from db.models import User

# registration function
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
        await User.create_user(
            db,
            telegram_id=telegram_id,
            language_code=message.from_user.language_code,
            username=username,
            first_name=first_name,
            last_name=last_name
        )

    else:
        return
