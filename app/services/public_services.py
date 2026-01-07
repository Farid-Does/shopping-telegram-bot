# In this file, services are created that are public and can be used in any type of handler.

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Category, Product




# returns products list to edit product information
# async def get_products_list_to_edit(db: AsyncSession, category_title: str):
#     category = await Category.get_by_title(db, category_title)
#     if not category:
#         bot_answer = "Invalid category"
#         products = []
#         return bot_answer, products
#     products = await Product.get_by_category_id(db, category_id=category.id)
#     if not products:
#         bot_answer = "no products are available."
#         products = []
#         return bot_answer, products
#     bot_answer = "choose the product to edit:"
#     return bot_answer, products