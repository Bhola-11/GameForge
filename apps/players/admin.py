from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'level', 'total_playtime_hours', 'country_code', 'is_banned', 'created_at')
    list_filter = ('is_banned', 'country_code')
    search_fields = ('username', 'email')
