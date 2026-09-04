from django.contrib import admin
from .models import Task, TaskComment, TaskTimeLog, TaskSprint

class CommentInline(admin.TabularInline):
    model = TaskComment
    extra = 0

class TimeLogInline(admin.TabularInline):
    model = TaskTimeLog
    extra = 0

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'task_type', 'status', 'priority', 'assigned_to', 'due_date')
    list_filter = ('status', 'priority', 'task_type', 'project')
    search_fields = ('title', 'description')
    inlines = [CommentInline, TimeLogInline]

admin.site.register(TaskSprint)
admin.site.register(TaskComment)
admin.site.register(TaskTimeLog)
