from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class AddToCartFSM(StatesGroup):
    category = State()
    product = State()
    quantity = State()


class CartFSM(StatesGroup):
    edit = State()
    confirm = State()


class CheckoutFSM(StatesGroup):
    address = State()
    shipping_method = State()
    confirm = State()


class AddAddressFSM(StatesGroup):
    city = State()
    address_text = State()
    postal_code = State()