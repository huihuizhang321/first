from django.contrib import admin
from .models import Customer, Contact, Deal, Task


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'status', 'email', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'company', 'email']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer', 'role', 'email', 'is_primary']
    list_filter = ['is_primary']
    search_fields = ['name', 'email']


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'value', 'stage', 'expected_close']
    list_filter = ['stage']
    search_fields = ['title']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'customer', 'priority', 'is_completed', 'due_date']
    list_filter = ['is_completed', 'priority']
    search_fields = ['title']
