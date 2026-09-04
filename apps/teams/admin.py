from django.contrib import admin
from .models import Team, TeamMember, TeamSkill, TeamWorkload

class TeamMemberInline(admin.TabularInline):
    model = TeamMember
    extra = 1

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'lead', 'color_code')
    inlines = [TeamMemberInline]

admin.site.register(TeamMember)
admin.site.register(TeamSkill)
admin.site.register(TeamWorkload)
