from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




starter_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="help")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)