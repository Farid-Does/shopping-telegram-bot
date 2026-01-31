# Converting models created with SQLAlchemy into models that can be defined in Django.

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models import Q
from django.utils import timezone
from aiogram.types import InputFile





# ------------------------------
# manager models
# ------------------------------

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError("username is required.")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    

# ------------------------------
# models
# ------------------------------

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)  # Unique Telegram ID
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    language_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    class Meta:
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
        db_table = "categories"

    def __str__(self):
        return self.title
    

class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "attributes"
        


class Option(models.Model):
    id = models.BigAutoField(primary_key=True)
    value = models.CharField(max_length=255)

    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, related_name="options", db_column="attribute_id")
    
    class Meta:
        db_table = "options"
        
    

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock_quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    categories = models.ManyToManyField(Category, related_name="products", db_table="product_category")
    options = models.ManyToManyField(Option, related_name="products", db_table="product_option")

    class Meta:
        db_table = "products"
        constraints = [
            models.CheckConstraint(
                condition=Q(discount_percent__isnull=True) |
                (Q(discount_percent__gte=0) & Q(discount_percent__lte=100)),
                name="check_discount_percent"
            ),
        ]

        def __str__(self):
            return self.title


class Image(models.Model):
    id = models.BigAutoField(primary_key=True)
    file_path = models.CharField(max_length=500, help_text="Enter the image file path: 'python manage.py makemigrations'", null=True, blank=True)

    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

    class Meta:
        db_table = "images"

    def __str__(self):
        return self.file_path
    

class MessageLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    message_type = models.CharField(max_length=255)
    content = models.CharField(max_length=4096)
    send_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")

    class Meta:
        db_table = "messages"

    def __str__(self):
        return f"Message {self.id} from {self.user}"
    

class Cart(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    products = models.ManyToManyField(Product, related_name="carts", through='CartProduct')
    
    class Meta:
        db_table = "cart"

    def __str__(self):
        return f"Cart {self.id} of {self.user}"
    

class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=50, default="pending")
    payment_status = models.CharField(max_length=50, default="unpaid")
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders", through="OrderProduct")

    class Meta:
        db_table = "orders"

    def __str__(self):
        return f"Order {self.id} by {self.user}"
    

class Address(models.Model):
    id = models.BigAutoField(primary_key=True)
    address_text = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")

    class Meta:
        db_table = "addresses"
        constraints = [ models.UniqueConstraint(fields=["user", "address_text"], name="uq_user_address") ]

    def __str__(self):
        return f"{self.address_text} ({self.user})"
    

class OrderShipping(models.Model):
    id = models.BigAutoField(primary_key=True)
    shipping_method = models.CharField(max_length=50, default="standard")
    shipping_status = models.CharField(max_length=50, default="pending")
    tracking_code = models.CharField(max_length=100, null=True, blank=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="shipping")
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name="shipping")

    class Meta:
        db_table = "shipping"

    def __str__(self):
        return f"Shipping {self.id} for Order {self.order.id}"
    

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    gateway = models.CharField(max_length=50, null=True, blank=True)
    transaction_ref = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50, default="pending")
    paid_at = models.DateTimeField(null=True, blank=True)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment")

    class Meta:
        db_table = "payment"

    def __str__(self):
        return f"Payment {self.id} for Order {self.order.id}"
    

# ------------------------------
# Interface models
# ------------------------------

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "cart_product"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        db_table = "order_product"

    
    


        
