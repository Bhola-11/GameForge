from django.contrib import admin
from .models import Bug, BugComment

class BugCommentInline(admin.TabularInline):
    model = BugComment
    extra = 0

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display = ('bug_id', 'title', 'game', 'severity', 'priority', 'status', 'assigned_to')
    list_filter = ('severity', 'status', 'priority', 'game')
    search_fields = ('bug_id', 'title', 'steps_to_reproduce')
    inlines = [BugCommentInline]

admin.site.register(BugComment)
