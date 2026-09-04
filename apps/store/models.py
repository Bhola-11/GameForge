from django.db import models
from apps.games.models import Game

class StoreListing(models.Model):
    class PlatformStore(models.TextChoices):
        STEAM = 'STEAM', 'Steam'
        EPIC = 'EPIC_GAMES', 'Epic Games Store'
        PLAYSTATION = 'PLAYSTATION_STORE', 'PlayStation Store'
        XBOX = 'XBOX_STORE', 'Xbox Store'
        NINTENDO = 'NINTENDO_ESHOP', 'Nintendo eShop'
        GOG = 'GOG', 'GOG.com'
        APPLE = 'APPLE_APP_STORE', 'Apple App Store'
        GOOGLE = 'GOOGLE_PLAY', 'Google Play Store'

    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        REVIEW = 'UNDER_REVIEW', 'Store Review'
        APPROVED = 'APPROVED', 'Approved by Platform'
        PUBLISHED = 'PUBLISHED', 'Published / Live'
        HIDDEN = 'HIDDEN', 'Hidden'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='store_listings')
    store = models.CharField(max_length=40, choices=PlatformStore.choices, default=PlatformStore.STEAM)
    headline = models.CharField(max_length=200)
    short_description = models.CharField(max_length=350)
    full_description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, default=59.99)
    discount_percentage = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PUBLISHED)
    store_url = models.URLField(blank=True)
    tags = models.CharField(max_length=255, default='Action, RPG, Open World, Co-op, Souls-like')
    
    # Specs
    min_cpu = models.CharField(max_length=150, default='Intel Core i5-8400 or AMD Ryzen 5 2600')
    min_gpu = models.CharField(max_length=150, default='NVIDIA GeForce GTX 1060 6GB or AMD Radeon RX 580')
    min_ram_gb = models.PositiveIntegerField(default=16)
    min_storage_gb = models.PositiveIntegerField(default=75)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['game', 'store']
        unique_together = ('game', 'store')

    def __str__(self):
        return f"{self.game.title} on {self.get_store_display()}"
