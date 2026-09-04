from django.db import models
from django.conf import settings
from django.utils.text import slugify
from apps.organizations.models import Organization

class Team(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='teams')
    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_teams')
    description = models.TextField(blank=True)
    color_code = models.CharField(max_length=20, default='#3B82F6')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        unique_together = ('organization', 'name')

    def __str__(self):
        return f"{self.organization.name} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='team_memberships')
    role_in_team = models.CharField(max_length=80, default='Core Contributor')
    allocation_percentage = models.PositiveIntegerField(default=100, help_text="Workload allocation in percentage (e.g. 100%)")
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.team.name}"


class TeamSkill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, default='Programming', choices=[
        ('Programming', 'Programming / Systems'),
        ('Art3D', '3D Modeling & Animation'),
        ('Audio', 'Sound Design & Music'),
        ('QA', 'Quality Assurance & Testing'),
        ('Design', 'Game & Level Design'),
        ('DevOps', 'DevOps & Build Engineering'),
    ])

    def __str__(self):
        return f"{self.name} ({self.category})"


class TeamWorkload(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='workload_logs')
    week_start = models.DateField()
    capacity_hours = models.PositiveIntegerField(default=160)
    booked_hours = models.PositiveIntegerField(default=120)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-week_start']

    def __str__(self):
        return f"{self.team.name} Workload for {self.week_start}"
