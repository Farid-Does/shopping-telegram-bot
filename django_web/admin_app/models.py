# Converting models created with SQLAlchemy into models that can be defined in Django.

from django.db import models




# ------------------------------
# models
# ------------------------------

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    telegram_id = models.BigIntegerField(unique=True)  # Unique Telegram ID
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    language_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        managed = False  # Do not manage this table with Django migrations
        db_table = "users"

    def __str__(self):
        return f"{self.username} ({self.telegram_id})"


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children"
    )

    class Meta:
        managed = False
        db_table = "categories"

    def __str__(self):
        return self.title
    

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(
        "Category",
        related_name="products"
    )

    class Meta:
        managed = False
        db_table = "products"

    def __str__(self):
        return self.title
    

class MessageLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="messages"  # Related messages for the user
    )
    message_type = models.CharField(max_length=255)
    content = models.CharField(max_length=4096)
    send_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "messages"

    def __str__(self):
        return f"Message {self.id} from {self.user}"
    

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="carts"  # Related carts for the user
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "cart"

    def __str__(self):
        return f"Cart {self.id} of {self.user}"
    

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="orders"  # Related orders for the user
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, default="pending")
    payment_status = models.CharField(max_length=50, default="unpaid")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "orders"

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    

class OrderShipping(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.OneToOneField(
        "Order",
        on_delete=models.CASCADE,
        related_name="shipping"  # One-to-one relation with Order
    )
    address = models.ForeignKey(
        "Address",
        on_delete=models.CASCADE,
        related_name="shippings"  # Related shippings for the address
    )
    shipping_method = models.CharField(max_length=50, default="standard")
    shipping_status = models.CharField(max_length=50, default="pending")
    tracking_code = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        managed = False
        db_table = "shipping"

    def __str__(self):
        return f"Shipping {self.id} for Order {self.order.id}"
    

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    order = models.OneToOneField(
        "Order",
        on_delete=models.CASCADE,
        related_name="payment"  # One-to-one relation with Order
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway = models.CharField(max_length=50, null=True, blank=True)
    transaction_ref = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False  # Do not manage this table with Django migrations
        db_table = "payment"

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
    

class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        related_name="addresses"  # Related addresses for the user
    )
    address_text = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "addresses"
        constraints = [
            models.UniqueConstraint(fields=["user", "address_text"], name="uq_user_address")
        ]

    def __str__(self):
        return f"{self.address_text} ({self.user})"
