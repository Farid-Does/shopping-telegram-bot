from db.models import Category, Product
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Category





# show_category_products_handler handler service
async def get_category_all_products(message, db, category_title: str):
    category = await Category.get_by_title(db, category_title)
    if not category:
        bot_answer = "Invalid category."
        products = []
        return bot_answer, products
    products = await Product.get_by_category_id(db, category.id)
    if not products:
        bot_answer = "there's no products."
        products = []
        return bot_answer, products
    else:
        bot_answer = f"{category.title} category products:"
        products=products
        return bot_answer, products



# show_categories_handler handler service
async def get_all_categories(message: Message, db: AsyncSession):
    categories = await Category.get_all_title(db)
    if not categories:
        bot_answer = "categories are unavailable."
    else:
        bot_answer = "choose your desired category:"
    
    return bot_answer

