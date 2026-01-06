# handlers

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import os
from services.admin_services import check_admin
from filters.admin_filters import IsAdminFilter
from states.admin_states import AddProductFSM, UpdateProductFSM, StartingPoint
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from services.admin_services import validate_and_save_product
from keyboards.static_keyboard import crud_keyboard
from keyboards.keyboard_builders import category_keyboard_maker, product_keyboard_maker_web_type
from services.public_services import get_products_list_to_edit


admins = list(map(int, os.getenv("ADMINS").split(",")))

admin_router = Router()

# approved as an admin user
@admin_router.message(Command("admin"))
async def register_admin(message: Message, db: AsyncSession):
    user_telegram_id = message.from_user.id
    bot_answer = await check_admin(message, db, user_telegram_id, admins)
    await message.answer(bot_answer)

@admin_router.message(Command("crud"), IsAdminFilter())
async def crud_handler(message: Message, state: FSMContext):
    await message.answer("please select the desired operation:", reply_markup=crud_keyboard)
    await state.set_state(StartingPoint.start)
    


# handler, starting add product operation
@admin_router.message(StartingPoint.start, F.text == "Add product")
async def handle_start_add(message: Message, state: FSMContext, db: AsyncSession):
    keyboard = await category_keyboard_maker(db)
    await message.answer("please select the product category:", reply_markup=keyboard)
    await state.set_state(AddProductFSM.category)


@admin_router.message(AddProductFSM.category)
async def handle_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("what is your product name?")
    await state.set_state(AddProductFSM.title)


@admin_router.message(AddProductFSM.title)
async def handle_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("please write a description of your product:")
    await state.set_state(AddProductFSM.description)


@admin_router.message(AddProductFSM.description)
async def handle_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("enter your product price in dollars:")
    await state.set_state(AddProductFSM.price)


@admin_router.message(AddProductFSM.price)
async def handle_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("how many units of your desired product are available?")
    await state.set_state(AddProductFSM.stock_quantity)


@admin_router.message(AddProductFSM.stock_quantity)
async def handle_stock_quantity(message: Message, state: FSMContext):
    await state.update_data(stock_quantity=message.text)
    await message.answer("please choose and upload an image for product:")
    await state.set_state(AddProductFSM.image)


@admin_router.message(AddProductFSM.image)
async def handle_image(message: Message, state: FSMContext, db: AsyncSession):
    await state.update_data(image=message)

    # validate ans save
    data = await state.get_data()
    bot_answer = await validate_and_save_product(message, db, data)
    await message.answer(bot_answer)
    await state.clear()


# handler, starting edit product operation


    
