from django.contrib import admin
from admin_app import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "first_name", "last_name", "username", "phone_number", "created_at", "is_admin", "is_blocked",)
    list_filter = ("is_admin", "is_blocked",)
    search_fields = ("username", "first_name", "last_name",)
    ordering = ("id",)


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "parent",)
    list_filter = ("parent",)
    search_fields = ("title",)
    ordering = ("id",)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "category_list", "title", "price", "discount_price", "stock_quantity", "is_active", "created_at",)
    # ManyToManyField 'categories' را نمی‌توان مستقیم list_filter گذاشت
    list_filter = ("discount_price", "stock_quantity", "is_active",)
    search_fields = ("title",)
    ordering = ("id",)

    def category_list(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])
    category_list.short_description = "Categories"


@admin.register(models.MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.MessageLog._meta.fields]
    list_filter = ("user", "message_type",)
    # send_at یک DateTimeField هست، جستجو ندارد → حذف یا فیلد متنی اضافه کن
    search_fields = ("content", "message_type",)
    ordering = ("id",)


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at",)
    ordering = ("id",)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "order_status", "payment_status", "created_at",)
    list_filter = ("user", "order_status", "payment_status",)
    ordering = ("id",)
    search_fields = ("order_status", "payment_status",)


@admin.register(models.OrderShipping)
class OrderShippingAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "address", "shipping_method", "shipping_status", "tracking_code",)
    list_filter = ("shipping_method", "shipping_status",)
    search_fields = ("tracking_code",)
    ordering = ("id",)


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Payment._meta.fields]
    list_filter = ("order", "gateway", "status")
    ordering = ("id",)
    search_fields = ("gateway", "status",)


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.Address._meta.fields]
    list_filter = ("user", "city", "country")
    search_fields = ("address_text", "postal_code")
    ordering = ("id",)
