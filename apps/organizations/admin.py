from django.contrib import admin
from .models import Organization, Department, OrgMember, OrgInvitation

class OrgMemberInline(admin.TabularInline):
    model = OrgMember
    extra = 1

class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_tier', 'created_by', 'is_active', 'created_at')
    inlines = [DepartmentInline, OrgMemberInline]

admin.site.register(Department)
admin.site.register(OrgMember)
admin.site.register(OrgInvitation)
