from django.contrib import admin
from .models import ReportTemplate

@admin.register(ReportTemplate)
class ReportTemplateAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'created_at')
