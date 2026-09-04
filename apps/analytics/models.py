from django.db import models
from apps.games.models import Game
from apps.players.models import Player

class DailyMetric(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='daily_metrics')
    metric_date = models.DateField()
    dau = models.PositiveIntegerField(default=12500, help_text="Daily Active Users")
    mau = models.PositiveIntegerField(default=85000, help_text="Monthly Active Users")
    avg_fps = models.DecimalField(max_digits=5, decimal_places=1, default=59.4)
    crash_count = models.PositiveIntegerField(default=12)
    revenue_usd = models.DecimalField(max_digits=12, decimal_places=2, default=14500.00)
    new_installs = models.PositiveIntegerField(default=3400)

    class Meta:
        ordering = ['-metric_date']
        unique_together = ('game', 'metric_date')

    def __str__(self):
        return f"{self.game.title} Metrics for {self.metric_date}"


class GameAnalyticsEvent(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='telemetry_events')
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True, related_name='events')
    event_name = models.CharField(max_length=100)
    event_data_json = models.TextField(blank=True, default='{}')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.event_name} @ {self.timestamp}"
