# handlers

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from db.models import User, Category
from sqlalchemy.ext.asyncio import AsyncSession
from keyboards.start_keyboard import starter_keyboard



# Initial and long messages og the bot
bot_message1 = "Welcome\nplease click the 'help' button to learn more and contact me more easily."
bot_message2 = "Hello,\nI am a Telegram bot that you can control and use to purchase our online products."
bot_message3 = """"you can control and use me by sending these commands:
'/browsingstore' - explore teh store and our products.
'/myorders' - view you order history.
'/order' - order our products by this command.
'/myactiveorder' - view your active order.
'/deleteorder' - you can use this order to delete your order,
 but the order you want to delete must meet the cancellation
conditions.
Otherwise, unfortunately, your order can't be canceled.
'/callrequest' - for phone contact with the store.
"""






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

    await message.answer(bot_message1, reply_markup=starter_keyboard)


@start_router.message( F.text == "help" )
async def help_handler(message: Message):

    await message.answer(bot_message2)
    await message.answer(bot_message3)



    


    


    
    
