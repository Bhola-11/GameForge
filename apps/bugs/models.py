from django.db import models
from django.conf import settings
from apps.games.models import Game
from apps.projects.models import Project

class Bug(models.Model):
    class Severity(models.TextChoices):
        BLOCKER = 'BLOCKER', 'Blocker / Crash'
        CRITICAL = 'CRITICAL', 'Critical'
        MAJOR = 'MAJOR', 'Major'
        MINOR = 'MINOR', 'Minor'
        TRIVIAL = 'TRIVIAL', 'Trivial / Cosmetic'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        CONFIRMED = 'CONFIRMED', 'Confirmed by QA'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        FIXED = 'FIXED', 'Fixed / Code Merged'
        RETEST = 'RETEST', 'Ready for Retest'
        CLOSED = 'CLOSED', 'Closed / Verified'
        REOPENED = 'REOPENED', 'Reopened'

    bug_id = models.CharField(max_length=50, unique=True, blank=True)
    title = models.CharField(max_length=250)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='bugs')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='bugs')
    version_found = models.CharField(max_length=50, default='v0.1.0-dev')
    platform = models.CharField(max_length=50, default='Windows PC')
    severity = models.CharField(max_length=30, choices=Severity.choices, default=Severity.MAJOR)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.HIGH)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.OPEN)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reported_bugs')
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs')
    steps_to_reproduce = models.TextField()
    expected_result = models.TextField()
    actual_result = models.TextField()
    logs_or_stacktrace = models.TextField(blank=True)
    screenshot = models.ImageField(upload_to='bug_screenshots/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.bug_id or 'BUG'}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.bug_id:
            count = Bug.objects.count() + 1
            self.bug_id = f"BUG-{count:05d}"
        super().save(*args, **kwargs)


class BugComment(models.Model):
    bug = models.ForeignKey(Bug, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.bug.bug_id}"
