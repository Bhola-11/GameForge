from django.contrib import admin
from .models import Leaderboard, LeaderboardEntry

class EntryInline(admin.TabularInline):
    model = LeaderboardEntry
    extra = 1

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'metric_type', 'season_name', 'is_active')
    inlines = [EntryInline]

admin.site.register(LeaderboardEntry)
