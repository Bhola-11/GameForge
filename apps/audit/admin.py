from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'module', 'description', 'ip_address')
    list_filter = ('module', 'action')
    search_fields = ('description', 'action', 'user__username')
