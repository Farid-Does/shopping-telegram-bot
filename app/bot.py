# Telegram bot

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

BOT = Bot(TOKEN)
dp = Dispatcher()