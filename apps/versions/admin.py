from django.contrib import admin
from .models import GameVersion

@admin.register(GameVersion)
class GameVersionAdmin(admin.ModelAdmin):
    list_display = ('version_number', 'game', 'release_type', 'status', 'release_date')
    list_filter = ('release_type', 'status', 'game')
