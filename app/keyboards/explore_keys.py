from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup




# keyboard showing categories
async def categories_keyboard_maker(categories_list: list[str], per_row: int = 3):
    buttons = []

    for i in range(0, len(categories_list), per_row):
        row = [KeyboardButton(text=title) for title in categories_list[i:i+per_row]]
        buttons.append(row)

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


async def products_keyboard_maker(message: Message, products: list, category_title: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(
                    text=p.title,
                    callback_data=f"product:{p.id}"
                )
            ]
            for p in products
        ]
    )

    return keyboard