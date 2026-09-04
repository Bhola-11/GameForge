from django.contrib import admin
from .models import Game, GameMilestone

class MilestoneInline(admin.TabularInline):
    model = GameMilestone
    extra = 1

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'genre', 'engine', 'status', 'target_release_date')
    list_filter = ('status', 'engine', 'organization')
    search_fields = ('title', 'genre')
    inlines = [MilestoneInline]

admin.site.register(GameMilestone)
