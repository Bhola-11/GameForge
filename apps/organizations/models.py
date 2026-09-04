import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Organization(models.Model):
    class PlanTier(models.TextChoices):
        INDIE = 'INDIE', 'Indie Studio (Up to 5 seats)'
        PRO = 'PRO', 'Pro Studio (Up to 25 seats)'
        ENTERPRISE = 'ENTERPRISE', 'Enterprise AAA (Unlimited)'

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='org_logos/', blank=True, null=True)
    plan_tier = models.CharField(max_length=30, choices=PlanTier.choices, default=PlanTier.PRO)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_orgs')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, blank=True)
    lead = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_departments')
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('organization', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.organization.name} - {self.name}"


class OrgMember(models.Model):
    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Owner / Studio Head'
        ADMIN = 'ADMIN', 'Studio Admin'
        MANAGER = 'MANAGER', 'Project Producer'
        MEMBER = 'MEMBER', 'Staff Member'
        GUEST = 'GUEST', 'Contractor / Guest'

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='org_memberships')
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.MEMBER)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('organization', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.organization.name} ({self.role})"


class OrgInvitation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        DECLINED = 'DECLINED', 'Declined'
        EXPIRED = 'EXPIRED', 'Expired'

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='invitations')
    email = models.EmailField()
    role = models.CharField(max_length=30, choices=OrgMember.Role.choices, default=OrgMember.Role.MEMBER)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_invitations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.email} to {self.organization.name}"
