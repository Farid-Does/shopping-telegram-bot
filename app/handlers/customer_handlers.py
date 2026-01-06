# handlers

import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.models import Category
from aiogram.filters import StateFilter
from services.customer_services import get_all_categories, get_category_all_products
from keyboards.keyboard_builders import category_keyboard_maker, product_keyboard_maker


# bot exploring router
customer_router = Router()
# browsing store and products.
@customer_router.message(Command("order"))
async def show_categories_handler(message: Message, db: AsyncSession):
    bot_answer = await get_all_categories(message, db)
    keyboard = await category_keyboard_maker(db, per_row=3)
    await message.answer(bot_answer, reply_markup=keyboard)


# handling category titles response
# @customer_router.message()
# async def show_category_products_handler(message: Message, db: AsyncSession):
#     category_title = message.text
#     bot_answer, products = await get_category_all_products(message, db, category_title)
#     keyboard = await product_keyboard_maker(db, message, products, category_title)
#     await message.answer(bot_answer, reply_markup=keyboard)
    

