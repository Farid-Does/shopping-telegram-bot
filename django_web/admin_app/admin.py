from django.contrib import admin
from django.utils.html import format_html
from admin_app import models




class ImageInline(admin.StackedInline):
    model = models.Image
    extra = 1
    fields = ("product", "file_path")


class OptionInline(admin.StackedInline):
    model = models.Option
    extra = 1
    fields = ("attribute", "value")



@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "first_name", "last_name", "username", "phone_number", "created_at", "is_superuser", "is_staff", "is_blocked",)
    list_filter = ("is_superuser", "is_staff", "is_blocked",)
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
    list_display = ("id", "category_list", "title", "price", "discount_percent", "stock_quantity", "is_active", "created_at",)
    list_filter = ("discount_percent", "stock_quantity", "is_active",)
    search_fields = ("title",)
    ordering = ("id",)

    inlines = [ImageInline]

    def category_list(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])
    category_list.short_description = "Categories"


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file_path",)


    def category_list(self, obj):
        return ", ".join([c.title for c in obj.categories.all()])
    category_list.short_description = "Categories"




@admin.register(models.Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "name",)
    search_fields = ("name",)
    ordering = ("id",)


@admin.register(models.Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("id", "value", "attribute")
    search_fields = ("value",)
    ordering = ("id",)



    def  image_preview(self, obj):
        if obj.image_file_id:
            return format_html('<img src="/media/products/{}" width="100" />', obj.image_file_id)
        return "-"
    image_preview.short_description = "Preview"


@admin.register(models.MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.MessageLog._meta.fields]
    list_filter = ("user", "message_type",)
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
    list_filter = ("user", "city")
    search_fields = ("address_text", "postal_code")
    ordering = ("id",)
