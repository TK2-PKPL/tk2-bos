from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts.views import google_login, logout_view, debug_login
from core.views import home, dashboard, theme_settings, reset_theme, permission_denied_view

handler403 = "core.views.permission_denied_view"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("settings/theme/", theme_settings, name="theme_settings"),
    path("settings/theme/reset/", reset_theme, name="reset_theme"),
    path("auth/google/", google_login, name="google_login"),
    path("auth/logout/", logout_view, name="logout"),
    path("debug-login/<str:role>/", debug_login, name="debug_login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)