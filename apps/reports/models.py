from django.db import models
from django.conf import settings

class ReportTemplate(models.Model):
    class ReportType(models.TextChoices):
        STUDIO_EXECUTIVE = 'STUDIO_EXECUTIVE', 'Executive Studio Summary'
        QA_DEFECT_VELOCITY = 'QA_DEFECT_VELOCITY', 'QA Bug & Triage Velocity'
        REVENUE_AND_COMMERCE = 'REVENUE_AND_COMMERCE', 'Monetization & Sales Breakdown'
        DEVELOPMENT_BURNDOWN = 'DEVELOPMENT_BURNDOWN', 'Task & Sprint Velocity'
        PLAYER_ENGAGEMENT = 'PLAYER_ENGAGEMENT', 'Player Engagement & DAU'

    title = models.CharField(max_length=150)
    report_type = models.CharField(max_length=40, choices=ReportType.choices, default=ReportType.STUDIO_EXECUTIVE)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
