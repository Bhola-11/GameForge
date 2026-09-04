from django.contrib import admin
from .models import StoreListing

@admin.register(StoreListing)
class StoreListingAdmin(admin.ModelAdmin):
    list_display = ('game', 'store', 'price', 'discount_percentage', 'status')
    list_filter = ('store', 'status', 'game')
