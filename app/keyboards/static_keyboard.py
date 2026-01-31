from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton




# help button to start working with bot
def starter_keyboard(bot_answer: str):
    if "'help'" in bot_answer:
        keyboard = ReplyKeyboardMarkup(
            keyboard = [
                [KeyboardButton(text="help")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    else:
        keyboard = None
    
    return keyboard


# admin /crud command keyboard
crud_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="Add product"), KeyboardButton(text="Edit product"), KeyboardButton(text="Remove product")],
        [KeyboardButton(text="Add user"), KeyboardButton(text="Edit user"), KeyboardButton(text="Remove user")],
        [KeyboardButton(text="Add category"), KeyboardButton(text="Remove category")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# product details keyboard
product_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="+", callback_data="increase"), InlineKeyboardButton(text="-", callback_data="descrease")],
        [InlineKeyboardButton(text="back", callback_data="back_to_products")]
    ]
)


# keyboard with buttons for orders shipping methods
order_shipping_keyboard = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="a"), KeyboardButton(text="b"), KeyboardButton(text="c")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# order confirm keyboard
order_confirm_keyboard = InlineKeyboardMarkup(
    inline_keyboard = [
        [InlineKeyboardButton(text="confirm and payment", callback_data="confirm_payment"), InlineKeyboardButton(text="cancel", callback_data="cancel__order")]
    ]
)

