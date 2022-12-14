from django.contrib import admin
from django.db.models import BigAutoField
from django.db.models import AutoField
from .models import (
    Customer,
    Product,
    Cart,
    OrderPlaced
)

@admin.register(Customer)
class CustomerModeAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'phone_no', 'email', 'address']

@admin.register(Product)
class ProductModeAdmin (admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'category', 'p_image']

@admin.register(Cart)
class CartModeAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'size', 'order_date', 'status']

