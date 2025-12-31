# handlers

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.start_keyboard import starter_keyboard


# bot starting router
start_router = Router()

@start_router.message(Command("start"))
async def start_and_register_handler(message: Message, db: AsyncSession):
    telegram_id = message.from_user.id
    user = await User.get_user_by_telegram_id(db, telegram_id)
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

    await message.answer(f"Welcome\nplease click the 'help' button to learn more and contact me more easily.", reply_markup=starter_keyboard)
