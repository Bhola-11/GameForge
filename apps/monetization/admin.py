from django.contrib import admin
from .models import InGameItem, Transaction

@admin.register(InGameItem)
class InGameItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'sku', 'item_type', 'price', 'is_active')
    list_filter = ('item_type', 'game', 'is_active')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'player', 'game', 'amount', 'status', 'payment_gateway', 'created_at')
    list_filter = ('status', 'payment_gateway', 'game')
