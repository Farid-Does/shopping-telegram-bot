from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from db.models import Category
from sqlalchemy.ext.asyncio import AsyncSession




# creates keyboard with buttons for categories title
async def category_keyboard_maker(db: AsyncSession, per_row: int = 3):
    categories_list = await Category.get_all_title(db)
    buttons = []

    for i in range(0, len(categories_list), per_row):
        row = [KeyboardButton(text=title) for title in categories_list[i:i+per_row]]
        buttons.append(row)

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


# creates inline keyboard with button for products
async def product_keyboard_maker(products: list[str], per_row: int = 3):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text=p.title, callback_data=f"product:{p.id}") for p in products[i: i+per_row]]
            for i in range(0, len(products), per_row)
        ]
    )

    return keyboard


