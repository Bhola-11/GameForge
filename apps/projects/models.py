from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.organizations.models import Organization
from apps.games.models import Game

class Project(models.Model):
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'Planning'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        ON_HOLD = 'ON_HOLD', 'On Hold'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='projects')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='projects')
    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_projects')
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.IN_PROGRESS)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.HIGH)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=100000.00)
    progress_percentage = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.game.title} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships')
    role_in_project = models.CharField(max_length=100, default='Developer')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f"{self.user.username} on {self.project.title}"


class ProjectRisk(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='risks')
    description = models.CharField(max_length=300)
    impact = models.CharField(max_length=20, default='HIGH', choices=[('LOW', 'Low'), ('MED', 'Medium'), ('HIGH', 'High'), ('CRITICAL', 'Critical')])
    probability = models.CharField(max_length=20, default='MED', choices=[('LOW', 'Low'), ('MED', 'Medium'), ('HIGH', 'High')])
    mitigation_plan = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Risk: {self.description[:40]}"
