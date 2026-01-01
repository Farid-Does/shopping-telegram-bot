# handlers

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
from services.admin_services import check_admin




load_dotenv("C:/Users/Asus/Desktop/aiogram/shop-bot/bot_long_messages.env")
admins = list(map(int, os.getenv("ADMINS").split(',')))


admin_router = Router()

# approved as an admin user
@admin_router.message(Command("admin"))
async def register_admin(message: Message, db: AsyncSession):
    user_telegram_id = message.from_user.id
    bot_answer = await check_admin(message, db, user_telegram_id, admins)
    await message.answer(bot_answer)