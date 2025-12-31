from aiogram import Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from keyboards.explore_keys import categories_keyboard_maker, products_keyboard_maker
from services.category_services import get_products_by_category_title
import asyncio
from db.models import Category

# bot exploring router
explore_router = Router()

# first use of exploring router
@explore_router.message(Command("browsingstore"))
async def show_categories(message: Message, db: AsyncSession):
    categories_list = await Category.get_all_title(db)
    if not categories_list:
        await message.answer("categories are unavailable.")
        return
    keyboard = await categories_keyboard_maker(categories_list, per_row=3)
    await message.answer("choose your desired category:", reply_markup=keyboard)


# handling category titles response
@explore_router.message(F.text)
async def category_handler(message: Message, db: AsyncSession):
    category_title = message.text
    category, products = await get_products_by_category_title(db, message.text)

    if not category:
        await message.answer("Invalid category")
        return

    if not products:
        await message.answer("There's no products.")
        return

    await products_keyboard_maker(message, products, category_title)