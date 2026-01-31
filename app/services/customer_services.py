import re
from db.models import Category, Product, Cart, Address, Order, OrderShipping
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession




# ------------------------------------------------------------
# function_based services
# ------------------------------------------------------------







# ------------------------------------------------------------
# class_based services
# ------------------------------------------------------------

# cart services
class CartService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # show_categories_handler handler service
    async def categories_list_service(self, user_id: int):
        categories = await Category.get_all_title(self.db)
        if not categories:
            return {
                "ok" : False,
                "bot_answer" : "purchasing is not active.",
                "data" : []
            }
        
        return {
            "ok" : True,
            "bot_answer" : "choose your desired category:",
            "data" : categories
        }
    
    # choose_category_handler handler service: returns products list too
    async def products_list_service(self, category_id: int):
        products = await Product.get_category_all_products()
        if not products:
            return {
                "ok" : False,
                "bot_answer" : "thers's no product in this category. please use order command again and choose another category.",
                "data" : []
            }
        
        return {
            "ok" : True,
            "bot_answer" : "choose the product you want:",
            "data" : products
        }
    
    # choose_product_handler handler service
    async def user_desired_product_service(self, product_id: int):
        quantity = await Product.get_product_quantity(self.db, product_id)
        if quantity is None:
            return {
                "ok" : False,
                "bot_answer" : "unavailable product"
            }
        
        return {
            "ok" : True,
            "bot_answer" : "product saved"
        }
    
    # create_cart_handler handler service
    async def create_cart_for_user(self, user_id: int, product_id: int):
        user_cart = await Cart.create_cart(self.db, user_id, product_id)
        return {
            "ok" : True,
            "bot_answer" : "this is your cart, and you can confirm ot edit it",
        }









    

  



    