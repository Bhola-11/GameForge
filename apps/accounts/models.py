import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        SUPER_ADMIN = 'SUPER_ADMIN', _('Super Admin')
        ORG_ADMIN = 'ORG_ADMIN', _('Organization Admin')
        PROJECT_MANAGER = 'PROJECT_MANAGER', _('Project Manager')
        LEAD_DEVELOPER = 'LEAD_DEVELOPER', _('Lead Developer')
        DEVELOPER = 'DEVELOPER', _('Developer')
        DESIGNER = 'DESIGNER', _('Designer / Artist')
        QA_TESTER = 'QA_TESTER', _('QA Tester')
        MARKETING_MANAGER = 'MARKETING_MANAGER', _('Marketing Manager')
        SUPPORT_AGENT = 'SUPPORT_AGENT', _('Support Agent')
        VIEWER = 'VIEWER', _('Viewer / Stakeholder')

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.DEVELOPER)
    department = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, default='Game Developer')
    phone = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    github_handle = models.CharField(max_length=100, blank=True)
    discord_tag = models.CharField(max_length=100, blank=True)
    api_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def display_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.username

    def is_lead_or_higher(self):
        return self.role in [
            self.Role.SUPER_ADMIN,
            self.Role.ORG_ADMIN,
            self.Role.PROJECT_MANAGER,
            self.Role.LEAD_DEVELOPER
        ] or self.is_superuser


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    theme = models.CharField(max_length=20, default='dark', choices=[('dark', 'Dark Cyber'), ('light', 'Clean Light')])
    email_notifications = models.BooleanField(default=True)
    task_assignment_alerts = models.BooleanField(default=True)
    bug_alerts = models.BooleanField(default=True)
    build_failure_alerts = models.BooleanField(default=True)
    compact_view = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
