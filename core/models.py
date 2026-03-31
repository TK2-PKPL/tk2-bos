from django.conf import settings
from django.db import models


PALETTE_CHOICES = [
    ("aurora", "Aurora Blue"),
    ("emerald", "Emerald Calm"),
    ("sunset", "Sunset Coral"),
    ("midnight", "Midnight Plum"),
]

FONT_CHOICES = [
    ("Inter", "Inter"),
    ("Poppins", "Poppins"),
    ("Lora", "Lora"),
    ("Space Grotesk", "Space Grotesk"),
]


class ThemeSetting(models.Model):
    singleton_key = models.PositiveSmallIntegerField(default=1, unique=True, editable=False)
    palette = models.CharField(max_length=20, choices=PALETTE_CHOICES, default="aurora")
    font_family = models.CharField(max_length=40, choices=FONT_CHOICES, default="Inter")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="theme_updates")
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(singleton_key=1)
        return obj


class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=120)
    detail = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
