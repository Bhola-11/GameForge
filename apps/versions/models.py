from django.db import models
from apps.games.models import Game

class GameVersion(models.Model):
    class ReleaseType(models.TextChoices):
        ALPHA = 'ALPHA', 'Alpha Prototype'
        BETA = 'BETA', 'Beta Preview'
        RC = 'RC', 'Release Candidate'
        MAJOR = 'MAJOR', 'Major Milestone (v1.0, v2.0)'
        MINOR = 'MINOR', 'Feature Update'
        PATCH = 'PATCH', 'Patch / Hotfix'

    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        ACTIVE = 'ACTIVE', 'Active Development'
        RELEASED = 'RELEASED', 'Released'
        DEPRECATED = 'DEPRECATED', 'Deprecated'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='versions')
    version_number = models.CharField(max_length=50, help_text="e.g. v1.2.0")
    release_type = models.CharField(max_length=30, choices=ReleaseType.choices, default=ReleaseType.MINOR)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)
    release_date = models.DateField(null=True, blank=True)
    changelog = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('game', 'version_number')

    def __str__(self):
        return f"{self.game.title} - {self.version_number}"
