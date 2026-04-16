from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_editable = ['is_active']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'unit', 'stock_quantity', 'is_available']
    list_editable = ['price', 'stock_quantity', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name']
# Register your models here.
