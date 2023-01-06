from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "pk",
        "price",
        "description",
        "owner",
        "buyer",
        "kind",
        "is_reported",
    )
