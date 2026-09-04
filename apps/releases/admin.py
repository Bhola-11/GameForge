from django.contrib import admin
from .models import Release, ReleaseChecklist

class ChecklistInline(admin.TabularInline):
    model = ReleaseChecklist
    extra = 1

@admin.register(Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('release_code', 'title', 'game', 'status', 'scheduled_date', 'published_date')
    list_filter = ('status', 'game')
    inlines = [ChecklistInline]

admin.site.register(ReleaseChecklist)
