from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'user', 'amount',
                    'payment_method', 'payment_status', 'paid_at']
    list_filter = ['payment_status', 'payment_method']
    readonly_fields = ['created_at']

# Register your models here.
