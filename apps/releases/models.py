from django.db import models
from django.conf import settings
from apps.games.models import Game
from apps.versions.models import GameVersion
from apps.builds.models import Build

class Release(models.Model):
    class Status(models.TextChoices):
        PLANNED = 'PLANNED', 'Planned'
        PREPARING = 'PREPARING', 'Preparing Staging'
        QA = 'QA', 'In Final QA Verification'
        APPROVED = 'APPROVED', 'Approved for Deployment'
        PUBLISHED = 'PUBLISHED', 'Published / Live'
        ROLLED_BACK = 'ROLLED_BACK', 'Rolled Back'

    release_code = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=200)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='releases')
    version = models.ForeignKey(GameVersion, on_delete=models.SET_NULL, null=True, related_name='releases')
    build = models.ForeignKey(Build, on_delete=models.SET_NULL, null=True, blank=True, related_name='releases')
    target_platform = models.CharField(max_length=100, default='Steam, PS5, Xbox Series X')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PLANNED)
    scheduled_date = models.DateTimeField()
    published_date = models.DateTimeField(null=True, blank=True)
    release_notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_releases')
    deployment_logs = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_releases')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"{self.game.title} - {self.release_code}: {self.title}"


class ReleaseChecklist(models.Model):
    release = models.ForeignKey(Release, on_delete=models.CASCADE, related_name='checklists')
    item_text = models.CharField(max_length=250)
    is_completed = models.BooleanField(default=False)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.item_text
