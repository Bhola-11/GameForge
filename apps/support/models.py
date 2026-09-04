from django.db import models
from django.conf import settings
from apps.players.models import Player

class SupportTicket(models.Model):
    class Category(models.TextChoices):
        BILLING = 'BILLING', 'Billing & Microtransactions'
        ACCOUNT = 'ACCOUNT', 'Account Recovery & Login'
        BUG_REPORT = 'BUG_REPORT', 'In-Game Glitch / Exploit'
        GAMEPLAY = 'GAMEPLAY', 'Quest / Progression Blocker'
        BAN_APPEAL = 'BAN_APPEAL', 'Ban & Penalty Appeal'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        CRITICAL = 'CRITICAL', 'Critical'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        WAITING = 'WAITING', 'Waiting for Player'
        RESOLVED = 'RESOLVED', 'Resolved'
        CLOSED = 'CLOSED', 'Closed'

    ticket_id = models.CharField(max_length=40, unique=True, blank=True)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.GAMEPLAY)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.ticket_id}] {self.subject}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            count = SupportTicket.objects.count() + 1
            self.ticket_id = f"TICK-{count:05d}"
        super().save(*args, **kwargs)


class TicketMessage(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    is_staff = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply on {self.ticket.ticket_id}"
