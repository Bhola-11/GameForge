from django.db import models
from apps.games.models import Game
from apps.players.models import Player

class Achievement(models.Model):
    class Tier(models.TextChoices):
        BRONZE = 'BRONZE', 'Bronze'
        SILVER = 'SILVER', 'Silver'
        GOLD = 'GOLD', 'Gold'
        PLATINUM = 'PLATINUM', 'Platinum'
        SECRET = 'SECRET', 'Secret / Hidden'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='achievements')
    code = models.CharField(max_length=60)
    name = models.CharField(max_length=150)
    description = models.TextField()
    points = models.PositiveIntegerField(default=15)
    tier = models.CharField(max_length=30, choices=Tier.choices, default=Tier.BRONZE)
    icon_name = models.CharField(max_length=50, default='trophy-fill')
    is_hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['game', 'points']
        unique_together = ('game', 'code')

    def __str__(self):
        return f"{self.game.title} - {self.name} ({self.points} pts)"


class PlayerAchievement(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='unlocked_achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name='unlocks')
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'achievement')

    def __str__(self):
        return f"{self.player.username} unlocked {self.achievement.name}"
