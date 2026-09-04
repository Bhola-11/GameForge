from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=80)
    module = models.CharField(max_length=50)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.username if self.user else "System"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {user_str}: {self.action}"

    @classmethod
    def log_activity(cls, user, action, module, description, object_id='', ip_address=None):
        return cls.objects.create(
            user=user if getattr(user, 'is_authenticated', False) else None,
            action=action,
            module=module,
            description=description,
            object_id=str(object_id),
            ip_address=ip_address
        )
