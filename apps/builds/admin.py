from django.contrib import admin
from .models import Build

@admin.register(Build)
class BuildAdmin(admin.ModelAdmin):
    list_display = ('build_number', 'game', 'platform', 'status', 'branch_name', 'build_date')
    list_filter = ('platform', 'status', 'game')
    search_fields = ('build_number', 'branch_name', 'git_commit_hash')
