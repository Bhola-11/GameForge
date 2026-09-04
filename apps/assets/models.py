from django.db import models
from django.conf import settings
from apps.games.models import Game
from apps.projects.models import Project

class AssetTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.name}"


class Asset(models.Model):
    class Category(models.TextChoices):
        MODEL_3D = '3D_MODEL', '3D Model / Mesh'
        TEXTURE = 'TEXTURE', 'Texture / Material (PBR)'
        AUDIO = 'AUDIO', 'SFX / Sound Effect'
        MUSIC = 'MUSIC', 'Music / Soundtrack'
        UI = 'UI', 'UI / Iconography'
        VFX = 'VFX', 'VFX / Particle / Shader'
        ANIMATION = 'ANIMATION', 'Skeletal Animation'
        CONCEPT = 'CONCEPT', 'Concept Art / Storyboard'
        DOC = 'DOC', 'Design Doc / Script'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='assets')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='assets')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.MODEL_3D)
    file = models.FileField(upload_to='assets/', blank=True, null=True)
    file_size_mb = models.DecimalField(max_digits=8, decimal_places=2, default=12.5)
    format_extension = models.CharField(max_length=20, default='.fbx')
    version = models.CharField(max_length=30, default='v1.0')
    tags = models.ManyToManyField(AssetTag, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='owned_assets')
    poly_count = models.PositiveIntegerField(null=True, blank=True, help_text="For 3D Models")
    resolution = models.CharField(max_length=50, blank=True, help_text="e.g. 4096x4096")
    audio_duration_sec = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"
