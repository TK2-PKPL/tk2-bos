from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_EDITOR = "editor"
    ROLE_VIEWER = "viewer"
    ROLE_CHOICES = [
        (ROLE_EDITOR, "Editor"),
        (ROLE_VIEWER, "Viewer"),
    ]

    email = models.EmailField(unique=True)
    google_sub = models.CharField(max_length=255, unique=True, blank=True, null=True)
    avatar_url = models.URLField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VIEWER)
    display_name = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.get_full_name() or self.username
        super().save(*args, **kwargs)
