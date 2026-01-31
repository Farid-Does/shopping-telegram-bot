# In this file, services are created that are public and can be used in any type of handler.

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Category, Product, Address, Cart
import re
from decimal import Decimal, ROUND_HALF_UP




async def validate_and_show_order_information(db: AsyncSession, data: dict, user_id: int):
    """
    Validates user inputs and prepares final order confirmation data.
    Applies percentage discounts and cart quantities.
    """

    # --------------------------------------------------
    # user inputs
    # --------------------------------------------------
    city = data.get("city")
    address_text = data.get("address_text")
    phone_number = data.get("phone_number")
    postal_code = data.get("postal_code")
    shipping = data.get("shipping")

    # --------------------------------------------------
    # required fields check
    # --------------------------------------------------
    required_fields = {
        "city": city,
        "address_text": address_text,
        "phone_number": phone_number,
        "postal_code": postal_code,
        "shipping": shipping,
    }

    missing = [key for key, value in required_fields.items() if not value]
    if missing:
        return {
            "ok": False,
            "error_type": "missing_fields",
            "message": f"Missing required fields: {', '.join(missing)}"
        }

    # --------------------------------------------------
    # data cleaning
    # --------------------------------------------------
    phone_number = phone_number.replace("-", "").replace("_", "").replace(".", "").replace(" ", "")
    postal_code = postal_code.replace("-", "").replace("_", "").replace(".", "").replace(" ", "")

    # --------------------------------------------------
    # validation
    # --------------------------------------------------
    invalid = []

    if not city.isalpha():
        invalid.append("city name (only letters).")

    if address_text.strip() == "" or not re.search(r"[A-Za-z]", address_text):
        invalid.append(
            "address text (must contain at least one letter, not only numbers or symbols)."
        )

    if not phone_number.isdigit():
        invalid.append("phone number (only numbers).")

    if not postal_code.isdigit():
        invalid.append("postal code (only numbers).")

    if invalid:
        return {
            "ok": False,
            "error_type": "invalid_inputs",
            "message": "Invalid inputs:\n" + "\n".join(invalid)
        }

    # --------------------------------------------------
    # database checks
    # --------------------------------------------------
    user_cart = await Cart.get_by_user_id(db, user_id)
    if not user_cart or not user_cart.products:
        return {
            "ok": False,
            "error_type": "empty_cart",
            "message": "Your cart is empty."
        }

    user_address = await Address.get_by_postal_code(db, postal_code)
    if not user_address:
        return {
            "ok": False,
            "error_type": "address_not_found",
            "message": "Address with this postal code was not found."
        }

    # --------------------------------------------------
    # order price calculation
    # --------------------------------------------------
    products_summary = []
    total_price = Decimal("0.00")

    for item in user_cart.products:
        product = item.product   # Product object
        quantity = item.quantity # from cart_product table

        base_price = product.price

        # apply percentage discount if exists
        if product.discount_price:
            discount_percent = Decimal(product.discount_price) / Decimal("100")
            discounted_price = base_price * (Decimal("1.00") - discount_percent)
        else:
            discounted_price = base_price

        discounted_price = discounted_price.quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

        line_total = discounted_price * quantity
        total_price += line_total

        products_summary.append({
            "product_id": product.id,
            "title": product.title,
            "unit_price": base_price,
            "discount_percent": product.discount_price,
            "final_unit_price": discounted_price,
            "quantity": quantity,
            "line_total": line_total,
        })

    # --------------------------------------------------
    # final response (ready for confirmation)
    # --------------------------------------------------
    return {
        "ok": True,
        "user_id": user_id,
        "address": {
            "city": city,
            "address_text": address_text,
            "postal_code": postal_code,
        },
        "phone_number": phone_number,
        "shipping": shipping,
        "products": products_summary,
        "total_price": total_price.quantize(Decimal("0.01")),
    }





