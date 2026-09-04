from django.contrib import admin
from .models import Asset, AssetTag

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'category', 'format_extension', 'version', 'owner', 'created_at')
    list_filter = ('category', 'game')
    search_fields = ('title', 'description')

admin.site.register(AssetTag)
