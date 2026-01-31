# handlers

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from django_web.admin_app.models import User, Category
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.static_keyboard import starter_keyboard
from services.start_services import register
from dotenv import load_dotenv
import os


load_dotenv("C:/Users/Asus/Desktop/aiogram/shop-bot/bot_long_messages.env")


bot_message2 = os.getenv("MESSAGE2")
bot_message3 = os.getenv("MESSAGE3")




# bot starting router
start_router = Router()

@start_router.message(Command("start"))
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    bot_answer = await register(message, telegram_id)
    keyboard = starter_keyboard(bot_answer)
    await message.answer(bot_answer, reply_markup=keyboard)


# sending interactive commands to the Telegram bot.
@start_router.message( F.text == "help" )
async def help_handler(message: Message):
    await message.answer(bot_message2)
    await message.answer(bot_message3)



    

    
