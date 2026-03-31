from django.contrib import admin
from .models import ThemeSetting, AuditLog
admin.site.register(ThemeSetting)
admin.site.register(AuditLog)
