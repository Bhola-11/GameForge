import uuid
from django.db import models
from apps.games.models import Game
from apps.players.models import Player

class InGameItem(models.Model):
    class ItemType(models.TextChoices):
        SKIN = 'COSMETIC_SKIN', 'Hero / Weapon Skin'
        BATTLE_PASS = 'BATTLE_PASS', 'Seasonal Battle Pass'
        CURRENCY = 'CURRENCY_PACK', 'Virtual Gems / Gold Pack'
        DLC = 'DLC_EXPANSION', 'Expansion Story Pack'
        CONSUMABLE = 'CONSUMABLE', 'XP Boost / Consumable'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='store_items')
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=80, unique=True)
    item_type = models.CharField(max_length=30, choices=ItemType.choices, default=ItemType.SKIN)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=9.99)
    currency = models.CharField(max_length=10, default='USD')
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['game', 'name']

    def __str__(self):
        return f"{self.name} (${self.price})"


class Transaction(models.Model):
    class Status(models.TextChoices):
        COMPLETED = 'COMPLETED', 'Completed'
        PENDING = 'PENDING', 'Pending'
        REFUNDED = 'REFUNDED', 'Refunded'
        FAILED = 'FAILED', 'Failed / Declined'

    class Gateway(models.TextChoices):
        STEAM = 'STEAM_WALLET', 'Steam Microtransactions'
        STRIPE = 'STRIPE', 'Stripe Direct'
        PLAYSTATION = 'PSN', 'PlayStation Network'
        XBOX = 'XBOX_LIVE', 'Xbox Live Marketplace'

    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='transactions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='transactions')
    item = models.ForeignKey(InGameItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='sales')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.COMPLETED)
    payment_gateway = models.CharField(max_length=30, choices=Gateway.choices, default=Gateway.STEAM)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"${self.amount} by {self.player.username} ({self.status})"
