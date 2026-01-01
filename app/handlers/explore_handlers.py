# handlers

import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types import Message
from keyboards.explore_keys import categories_keyboard_maker, products_keyboard_maker
from services.explore_services import get_products_by_category_title
from states.explore_state import BrowseSteps
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.models import Category
from aiogram.filters import StateFilter
from services.explore_services import get_categories




# bot exploring router
explore_router = Router()
# browsing store and products.
@explore_router.message(Command("order"))
async def show_categories(message: Message, db: AsyncSession, state: FSMContext):
    await get_categories(message, db, state)
    await state.set_state(BrowseSteps.product_details)


# handling category titles response
@explore_router.message(F.text, StateFilter(BrowseSteps.product_details))
async def category_handler(message: Message, db: AsyncSession):
    category_title = message.text
    bot_answer, keyboard = await get_products_by_category_title(message, db, category_title)
    await message.answer(bot_answer, reply_markup=keyboard)
    

