import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from keyboards.explore_keys import categories_keyboard_maker, products_keyboard_maker
from services.category_services import get_products_by_category_title
from states.explore_state import BrowseSteps
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.models import Category
from aiogram.filters import StateFilter


# bot exploring router
explore_router = Router()

# first use of exploring router
@explore_router.message(Command("browsingstore"))
async def show_categories(message: Message, db: AsyncSession, state: FSMContext):
    current_state = await state.set_state(BrowseSteps.category_products)
    categories_list = await Category.get_all_title(db)
    if not categories_list:
        await message.answer("categories are unavailable.")
        await state.clear()
        return
    keyboard = await categories_keyboard_maker(categories_list, per_row=3)
    await message.answer("choose your desired category:", reply_markup=keyboard)
    await state.set_state(BrowseSteps.product_details)


# handling category titles response
@explore_router.message(F.text, StateFilter(BrowseSteps.product_details))
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