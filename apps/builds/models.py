from django.db import models
from django.conf import settings
from apps.games.models import Game

class Build(models.Model):
    class Platform(models.TextChoices):
        WIN64 = 'WINDOWS_X64', 'Windows (x64)'
        LINUX = 'LINUX_X64', 'Linux (x86_64)'
        MACOS = 'MACOS_ARM64', 'macOS (Apple Silicon)'
        PS5 = 'PS5', 'PlayStation 5'
        XBOX = 'XBOX_SERIES', 'Xbox Series X/S'
        SWITCH = 'NINTENDO_SWITCH', 'Nintendo Switch'
        ANDROID = 'ANDROID_APK', 'Android (AAB / APK)'
        IOS = 'IOS_IPA', 'iOS (IPA)'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending in CI Queue'
        BUILDING = 'BUILDING', 'Compiling / Cooking'
        SUCCESSFUL = 'SUCCESSFUL', 'Build Successful'
        FAILED = 'FAILED', 'Build Failed / Cook Error'
        TESTING = 'TESTING', 'In Smoke Testing'
        APPROVED = 'APPROVED', 'QA Approved for Release'
        REJECTED = 'REJECTED', 'QA Rejected'

    build_number = models.PositiveIntegerField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='builds')
    version = models.ForeignKey('versions.GameVersion', on_delete=models.SET_NULL, null=True, blank=True, related_name='builds')
    platform = models.CharField(max_length=40, choices=Platform.choices, default=Platform.WIN64)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SUCCESSFUL)
    git_commit_hash = models.CharField(max_length=64, default='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
    branch_name = models.CharField(max_length=100, default='main')
    file_size_mb = models.DecimalField(max_digits=8, decimal_places=2, default=1420.00)
    developer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_builds')
    qa_tester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='tested_builds')
    qa_notes = models.TextField(blank=True)
    build_duration_sec = models.PositiveIntegerField(default=480)
    build_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-build_date']
        unique_together = ('game', 'build_number')

    def __str__(self):
        return f"{self.game.title} - Build #{self.build_number} ({self.get_platform_display()})"
