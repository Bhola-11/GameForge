from django.db import models
from django.utils.text import slugify
from apps.games.models import Game
from apps.players.models import Player

class Leaderboard(models.Model):
    class MetricType(models.TextChoices):
        HIGH_SCORE = 'HIGH_SCORE', 'High Score (Points)'
        FASTEST_TIME = 'FASTEST_TIME', 'Speedrun / Time (Milliseconds)'
        KILL_COUNT = 'KILL_COUNT', 'Eliminations / Kills'
        LEVEL_REACHED = 'LEVEL_REACHED', 'Highest Wave / Level'
        WIN_STREAK = 'WIN_STREAK', 'Consecutive Win Streak'

    class SortOrder(models.TextChoices):
        DESC = 'DESC', 'Descending (Higher is better)'
        ASC = 'ASC', 'Ascending (Lower is better e.g. Speedrun)'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='leaderboards')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, blank=True)
    metric_type = models.CharField(max_length=30, choices=MetricType.choices, default=MetricType.HIGH_SCORE)
    sort_order = models.CharField(max_length=10, choices=SortOrder.choices, default=SortOrder.DESC)
    season_name = models.CharField(max_length=100, default='Season 1: Genesis')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['game', 'name']
        unique_together = ('game', 'slug')

    def __str__(self):
        return f"{self.game.title} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class LeaderboardEntry(models.Model):
    leaderboard = models.ForeignKey(Leaderboard, on_delete=models.CASCADE, related_name='entries')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='leaderboard_scores')
    score = models.BigIntegerField()
    formatted_score = models.CharField(max_length=50, default='10,000 pts')
    rank = models.PositiveIntegerField(default=1)
    achieved_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rank']
        unique_together = ('leaderboard', 'player')

    def __str__(self):
        return f"#{self.rank} {self.player.username}: {self.formatted_score}"
