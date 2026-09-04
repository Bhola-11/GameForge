import uuid
from django.db import models

class Player(models.Model):
    player_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=60, unique=True)
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(blank=True)
    country_code = models.CharField(max_length=10, default='US')
    is_banned = models.BooleanField(default=False)
    ban_reason = models.CharField(max_length=255, blank=True)
    total_playtime_hours = models.DecimalField(max_digits=8, decimal_places=1, default=0.0)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} (Lvl {self.level})"
