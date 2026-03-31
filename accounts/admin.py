from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Google profile", {"fields": ("google_sub", "avatar_url", "display_name", "role")}),)
    list_display = ("username", "email", "display_name", "role", "is_staff")
