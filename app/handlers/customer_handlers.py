# handlers

import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery, InputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from states.customer_states import AddToCartFSM, CartFSM, CheckoutFSM, AddAddressFSM
from keyboards.keyboard_builders import category_keyboard_maker, product_keyboard_maker




# customer router
customer_router = Router()



# show categories list
@customer_router.message(Command("order"))
async def show_categories_handler(message: Message, db: AsyncSession, state: FSMContext):
      pass


# user desired category handler
@customer_router.message(AddToCartFSM.category)
async def choose_category_handler(message: Message, db: AsyncSession, category_id: int, state: FSMContext):
       pass


# user desired product
@customer_router.message(AddToCartFSM.quantity)
async def choose_product_handler(message: Message, db : AsyncSession, state: FSMContext):
       pass


# creates cart for user
@customer_router.message(Command("createandeditcart"), "")
async def create_cart_handler(message: Message, db: AsyncSession, user_id: int, state: FSMContext):
      pass


# edit cart details: increase quantity
@customer_router.message(CartFSM.edit)
async def increase_product_quantity_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# edit cart details: descrease quantity
@customer_router.message(CartFSM.edit)
async def descraese_product_quantity_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# cart confirmation
@customer_router.message(CartFSM.confirm)
async def confirm_cart(message: Message, db: AsyncSession, state: FSMContext):
       pass


# user selected address
@customer_router.message(CheckoutFSM.address)
async def user_address_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# order shipping method
@customer_router.message(CheckoutFSM.shipping_method)
async def order_shipping_method_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# order information confirmation
@customer_router.message(CheckoutFSM.confirm)
async def confirm_cart_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# user address: city
@customer_router.message(AddAddressFSM.city)
async def address_city_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# user address: address text
@customer_router.message(AddAddressFSM.address_text)
async def address_text_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass


# user address: postal code
@customer_router.message(AddAddressFSM.postal_code)
async def address_postal_code_handler(message: Message, db: AsyncSession, state: FSMContext):
       pass








    

