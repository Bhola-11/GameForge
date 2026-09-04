from django.db import models
from apps.accounts.models import User

class RolePermission(models.Model):
    role = models.CharField(max_length=30, choices=User.Role.choices)
    module_name = models.CharField(max_length=50)
    can_view = models.BooleanField(default=True)
    can_create = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_approve_release = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'module_name')
        ordering = ['role', 'module_name']

    def __str__(self):
        return f"{self.role} -> {self.module_name}"
