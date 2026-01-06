# admin handlers services

from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User
from db.models import Product, Image, Category
import re





# register_admin handler service
async def check_admin(message: Message, db: AsyncSession, telegram_id: int, admins: list[int]):
    if telegram_id in admins:
        user = await User.get_full_record_by_telegram_id(db, telegram_id)
        user.is_admin = True
        bot_answer = "successfully saved as an admin."
    else:
        bot_answer = "unfortunately, your ID was not found in the admin ID list."
    return bot_answer




    
# validate_and_save_handler handler service: validates the inputs and saves teh record.
async def validate_and_save_product(message: Message, db: AsyncSession, data: dict):
    # new product information
    category_title = data.get("category")
    title = data.get("title")
    description = data.get("description")
    price = data.get("price")
    stock_quantity = data.get("stock_quantity")
    image = data.get("image")

    # validation
    invalid = []
    title_pattern = r'^[A-Za-z ]+$'
    description_pattern = r'^[\s\S]+$'

    if not re.match(title_pattern, title) or not re.search(r'[A-Za-z]', title):
        invalid.append("product title (only letters).")
    if not re.match(description_pattern, description) \
            or description.strip() == "" \
            or not re.search(r'[A-Za-z]', description):
        invalid.append(
        "product description (must contain at least one letter, not only numbers or symbols)."
    )

    
    try:
        quantity = int(stock_quantity)
        if quantity < 0:
            invalid.append("stock quantity (can't be under zero).")
    except ValueError:
        invalid.append("stock quantity (only positive integer or zero).")


    if not image.photo:
        invalid.append("product image (input must be an image).")

    if invalid:
        bot_answer = "Invalid inputs:\n" + "\n".join(invalid)
    else:
        category = await Category.get_by_title(db, category_title)
        category_id = category.id
        new_product = await Product.add_product(
            db,
            category_id=category_id,
            title=title,
            description=description,
            price=float(price),
            discount_price=float(0),
            stock_quantity=int(stock_quantity)
        )
        await db.flush()
        image_file_id = image.photo[-1].file_id
        await Image.add_image(db, product_id=new_product.id, image_file_id=image_file_id, sort_order=None)
        bot_answer = "your product has been successfully saved."
    return bot_answer





