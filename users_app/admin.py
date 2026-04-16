from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone_number', 'email', 'is_active', 'created_at']
    search_fields = ['full_name', 'phone_number']
    list_filter = ['is_active']

# Register your models here.
