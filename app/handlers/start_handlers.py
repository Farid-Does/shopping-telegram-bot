# handlers

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from db.models import User, Category
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.start_keyboard import starter_keyboard
from services.registration_service import register
from dotenv import load_dotenv
import os

load_dotenv()
admins = list(map(int, os.getenv("ADMINS").split(',')))



# Initial and long messages og the bot
bot_message1 = "Welcome\nplease click the 'help' button to learn more and contact me more easily."
bot_message2 = "Hello,\nI am a Telegram bot that you can control and use to purchase our online products."
bot_message3 = """"you can control and use me by sending these commands:
/browsingstore - explore teh store and our products.
/myorders - view you order history.
/order - order our products by this command.
/myactiveorder - view your active order.
/deleteorder - you can use this order to delete your order,
 but the order you want to delete must meet the cancellation
conditions.
Otherwise, unfortunately, your order can't be canceled.
/callrequest - for phone contact with the store.
/admin - using this command, you can be approved as an admin and operate.
"""






# bot starting routers
start_router = Router()
admin_router = Router()

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


# approved as an admin user
@admin_router.message(Command("admin"))
async def register_admin(message: Message, db: AsyncSession):
    user_telegram_id = message.from_user.id
    
    if user_telegram_id in admins:
        user = await User.get_full_record_by_telegram_id(db, user_telegram_id)
        user.is_admin = True
        bot_answer = "successfully saved as an admin."
    else:
        bot_answer = "unfortunately, your ID was not found in the admin ID list."
    await message.answer(bot_answer)
    


    
    
