from django.contrib import admin
from .models import Achievement, PlayerAchievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'code', 'tier', 'points', 'is_hidden', 'is_active')
    list_filter = ('tier', 'game', 'is_hidden', 'is_active')

admin.site.register(PlayerAchievement)
