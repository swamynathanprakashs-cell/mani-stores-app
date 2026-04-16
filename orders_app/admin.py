from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'quantity', 'unit_price', 'subtotal']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_status', 'total_amount',
                    'payment_method', 'payment_status', 'token_number', 'placed_at']
    list_filter = ['order_status', 'payment_status', 'payment_method']
    readonly_fields = ['placed_at', 'token_number']
    inlines = [OrderItemInline]

# Register your models here.
