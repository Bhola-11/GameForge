from django.contrib import admin
from .models import RolePermission

@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'module_name', 'can_view', 'can_create', 'can_edit', 'can_delete', 'can_approve_release')
    list_filter = ('role', 'module_name')
