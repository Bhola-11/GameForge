from django.contrib import admin
from .models import Project, ProjectMember, ProjectRisk

class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1

class ProjectRiskInline(admin.TabularInline):
    model = ProjectRisk
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'game', 'status', 'priority', 'progress_percentage', 'lead')
    list_filter = ('status', 'priority', 'game')
    inlines = [ProjectMemberInline, ProjectRiskInline]

admin.site.register(ProjectMember)
admin.site.register(ProjectRisk)
