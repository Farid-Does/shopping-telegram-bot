# handlers

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from db.models import User, Category
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.start_keyboard import starter_keyboard
from services.start_services import register
from dotenv import load_dotenv
import os




bot_message1 = os.getenv("MESSAGE1")
bot_message2 = os.getenv("MESSAGE2")
bot_message3 = os.getenv("MESSAGE3")



# bot starting router
start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: Message, db: AsyncSession):
    telegram_id = message.from_user.id
    await register(message, db, telegram_id)
    await message.answer(bot_message1, reply_markup=starter_keyboard)


# sending interactive commands to the Telegram bot.
@start_router.message( F.text == "help" )
async def help_handler(message: Message):
    await message.answer(bot_message2)
    await message.answer(bot_message3)



    

    
