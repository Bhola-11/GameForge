from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.organizations.models import Organization

class Game(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'Planning & Concept'
        PRE_PRODUCTION = 'PRE_PRODUCTION', 'Pre-Production'
        PRODUCTION = 'PRODUCTION', 'Full Production'
        TESTING = 'TESTING', 'QA & Playtesting'
        BETA = 'BETA', 'Closed / Open Beta'
        RELEASED = 'RELEASED', 'Released / Live'
        MAINTENANCE = 'MAINTENANCE', 'LiveOps & Maintenance'
        ARCHIVED = 'ARCHIVED', 'Archived'

    class Engine(models.TextChoices):
        UNREAL_5 = 'UNREAL_5', 'Unreal Engine 5'
        UNITY_6 = 'UNITY_6', 'Unity 6'
        GODOT_4 = 'GODOT_4', 'Godot Engine 4'
        CUSTOM_CPP = 'CUSTOM_CPP', 'Custom Proprietary C++'
        CRYENGINE = 'CRYENGINE', 'CryEngine'

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='games')
    genre = models.CharField(max_length=100, default='Action RPG')
    engine = models.CharField(max_length=40, choices=Engine.choices, default=Engine.UNREAL_5)
    platforms = models.CharField(max_length=255, default='PC, PlayStation 5, Xbox Series X')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PRODUCTION)
    summary = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='game_covers/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='game_banners/', blank=True, null=True)
    target_release_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=500000.00)
    repository_url = models.URLField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_games')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GameMilestone(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=150)
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['due_date']

    def __str__(self):
        return f"{self.game.title} - {self.title}"
