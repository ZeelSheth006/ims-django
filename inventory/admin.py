from django.contrib import admin
from .models import Product, PurchaseBatch

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   list_display = ("name", "stock", "price")


@admin.register(PurchaseBatch)
class PurchaseBatchAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity_left", "price_per_unit", "created_at")
