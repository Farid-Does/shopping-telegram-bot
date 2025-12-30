# creating models


from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text, DateTime, Boolean, Numeric, DECIMAL, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property




# ------------------------------
# Base
# ------------------------------
class Base(DeclarativeBase):
    pass

# ------------------------------
# Interface tables
# ------------------------------


# Product ↔ Category
product_category = Table(
    "product_category",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True)
)

# Cart ↔ Product
cart_product = Table(
    "cart_product",
    Base.metadata,
    Column("cart_id", ForeignKey("cart.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1)
)

# Order ↔ Product (OrderItems)
order_items_table = Table(
    "order_items_assoc",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id"), primary_key=True),
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer, nullable=False, default=1),
    Column("price_at_purchase", Numeric(10,2), nullable=False)
)

# ------------------------------
# models
# ------------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone_number: Mapped[str | None] = mapped_column(unique=True)
    language_code: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    is_blocked: Mapped[bool] = mapped_column(default=False)

    messages: Mapped[list["MessageLog"]] = relationship(back_populates="user")
    orders: Mapped[list["Order"]] = relationship(back_populates="user")
    addresses: Mapped[list["Address"]] = relationship(back_populates="user")
    carts: Mapped[list["Cart"]] = relationship(back_populates="user")

    @hybrid_property
    def is_active(self):
        return not self.is_blocked

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))

    parent: Mapped["Category"] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list["Category"]] = relationship(back_populates="parent")
    products: Mapped[list["Product"]] = relationship(secondary=product_category, back_populates="categories")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    discount_price: Mapped[DECIMAL | None] = mapped_column(DECIMAL(5, 2))
    stock_quantity: Mapped[int] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    categories: Mapped[list["Category"]] = relationship(secondary=product_category, back_populates="products")
    images: Mapped[list["Image"]] = relationship(back_populates="product")
    orders: Mapped[list["OrderItems"]] = relationship(secondary=order_items_table, back_populates="products")
    carts: Mapped[list["Cart"]] = relationship(secondary=cart_product, back_populates="products")


class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    image_file_id: Mapped[str | None] = mapped_column(String, nullable=True)
    sort_order: Mapped[int | None] = mapped_column(Integer, nullable=True)

    product: Mapped["Product"] = relationship(back_populates="images")


class MessageLog(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    message_type: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(String(4096), nullable=False)
    send_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="messages")


class Cart(Base):
    __tablename__ = "cart"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="carts")
    products: Mapped[list["Product"]] = relationship(secondary=cart_product, back_populates="carts")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    total_price: Mapped[Numeric] = mapped_column(Numeric(10,2), nullable=False)
    order_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    payment_status: Mapped[str] = mapped_column(String(50), nullable=False, default="unpaid")
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="orders")
    shipping: Mapped["OrderShipping"] = relationship(back_populates="order", uselist=False)
    payment: Mapped["Payment"] = relationship(back_populates="order", uselist=False)
    products: Mapped[list["Product"]] = relationship(secondary=order_items_table, back_populates="orders")


class OrderItems(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    price_at_purchase: Mapped[Numeric] = mapped_column(Numeric(10,2), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    products: Mapped[list["Product"]] = relationship(secondary=order_items_table, back_populates="orders")


class OrderShipping(Base):
    __tablename__ = "shipping"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    address_id: Mapped[int] = mapped_column(ForeignKey("addresses.id"), nullable=False)
    shipping_method: Mapped[str] = mapped_column(String(50), nullable=False, default="standard")
    shipping_status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    tracking_code: Mapped[str | None] = mapped_column(String(100), nullable=True)

    order: Mapped["Order"] = relationship(back_populates="shipping")


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    amount: Mapped[Numeric] = mapped_column(Numeric(10,2), nullable=False)
    gateway: Mapped[str | None] = mapped_column(String(50), nullable=True)
    transaction_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    paid_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    order: Mapped["Order"] = relationship(back_populates="payment")


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    address_text: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    country: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="addresses")

    __table_args__ = (
        UniqueConstraint("user_id", "address_text", name="uq_user_address"),
    )
