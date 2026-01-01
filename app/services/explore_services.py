from db.models import Category, Product
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from states.explore_state import BrowseSteps
from db.models import Category
from aiogram.filters import StateFilter
from keyboards.explore_keys import categories_keyboard_maker, products_keyboard_maker




# category_handler handler service
async def get_products_by_category_title(message, db, title: str):
    category = await Category.get_by_title(db, title)
    if not category:
        bot_answer = "Invalid category."
        keyboard = None
        return bot_answer, keyboard
    products = await Product.get_by_category_id(db, category.id)
    keyboard = await products_keyboard_maker(message, products, category.title)
    if not products:
        bot_answer = "there's no products."
        keyboard = None
        return bot_answer, keyboard
    else:
        bot_answer = f"{category.title} category products:"
        keyboard = keyboard

    return bot_answer, keyboard



# show_categories handler service
async def get_categories(message: Message, db: AsyncSession, state: FSMContext):
    current_state = await state.set_state(BrowseSteps.category_products)
    categories_list = await Category.get_all_title(db)
    if not categories_list:
        await message.answer("categories are unavailable.")
        await state.clear()
        return
    keyboard = await categories_keyboard_maker(categories_list, per_row=3)
    await message.answer("choose your desired category:", reply_markup=keyboard)
