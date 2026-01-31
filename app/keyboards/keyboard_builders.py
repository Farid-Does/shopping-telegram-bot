from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from db.models import Category
from sqlalchemy.ext.asyncio import AsyncSession




# creates keyboard with buttons for categories title
async def category_keyboard_maker(categories: list[str], per_row: int = 3):
    buttons = []

    for i in range(0, len(categories), per_row):
        row = [KeyboardButton(text=title) for title in categories[i:i+per_row]]
        buttons.append(row)

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


# creates inline keyboard with button for products
def product_keyboard_maker(products: list[str], per_row: int = 3):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text=p.title, callback_data=f"product:{p.id}") for p in products[i: i+per_row]]
            for i in range(0, len(products), per_row)

            # two side buttons : back and continue
            [
                InlineKeyboardButton(text="back to categories", callback_data="back_to_categories"),
                InlineKeyboardButton(text="ok order", callback_data="ok_order")
            ]
        ]
    )

    return keyboard


# creates inline keyboard with buttons for addresses
def add_address_keyboard_maker(addresses: list[object], per_row: int = 1):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text=address.postal_code, callback_data=f"address:{address.id}") for address in addresses[i: i+per_row]]
            for i in range(0, len(addresses), per_row)

            # add new address button
            [InlineKeyboardButton(text="Add new address", callback_data="add_address")]
        ]
    )

    return keyboard














