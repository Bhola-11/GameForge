from django.db import models
from django.conf import settings

class Notification(models.Model):
    class Type(models.TextChoices):
        TASK_ASSIGNED = 'TASK_ASSIGNED', 'Task Assigned'
        BUG_FILED = 'BUG_FILED', 'Bug Reported / Assigned'
        BUILD_STATUS = 'BUILD_STATUS', 'Build Pipeline Alert'
        RELEASE_GATE = 'RELEASE_GATE', 'Release Stage Sign-Off'
        SUPPORT_REPLY = 'SUPPORT_REPLY', 'Support Desk Response'
        SYSTEM = 'SYSTEM', 'System Alert'

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=Type.choices, default=Type.SYSTEM)
    link = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient.username}: {self.title}"
