from django.contrib import admin
from .models import DailyMetric, GameAnalyticsEvent

@admin.register(DailyMetric)
class DailyMetricAdmin(admin.ModelAdmin):
    list_display = ('game', 'metric_date', 'dau', 'mau', 'avg_fps', 'revenue_usd')
    list_filter = ('game',)

admin.site.register(GameAnalyticsEvent)
