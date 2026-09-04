from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserPreference

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'job_title', 'department', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('GameForge Profile', {'fields': ('role', 'job_title', 'department', 'phone', 'avatar', 'bio', 'timezone', 'github_handle', 'discord_tag', 'api_key', 'is_verified')}),
    )

admin.site.register(UserPreference)
