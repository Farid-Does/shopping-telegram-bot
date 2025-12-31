from db.models import Category, Product

async def get_products_by_category_title(db, title: str):
    category = await Category.get_by_title(db, title)
    if not category:
        return None, None

    products = await Product.get_by_category_id(db, category.id)
    return category, products