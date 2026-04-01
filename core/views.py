from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .decorators import editor_required
from .forms import ThemeForm
from .models import AuditLog, ThemeSetting
from .utils import get_client_ip
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from social_django.utils import psa 


def home(request):
    return render(request, "core/home.html")

@login_required
def dashboard(request):
    return render(request, "core/dashboard.html", {"recent_logs": AuditLog.objects.select_related("actor")[:8]})

@editor_required
def theme_settings(request):
    theme = ThemeSetting.get_solo()
    if request.method == "POST":
        form = ThemeForm(request.POST)
        if form.is_valid():
            old_palette = theme.palette
            old_font = theme.font_family
            theme.palette = form.cleaned_data["palette"]
            theme.font_family = form.cleaned_data["font_family"]
            theme.updated_by = request.user
            theme.save()
            AuditLog.objects.create(actor=request.user, action="theme_update", detail=f"Tema diganti dari {old_palette} {old_font} menjadi {theme.palette} {theme.font_family}", ip_address=get_client_ip(request), user_agent=request.META.get("HTTP_USER_AGENT", "")[:255])
            messages.success(request, "Tema website berhasil diperbarui.")
            return redirect("theme_settings")
    else:
        form = ThemeForm(initial={"palette": theme.palette, "font_family": theme.font_family})
    return render(request, "core/theme_settings.html", {"form": form, "theme": theme})

@require_POST
@editor_required
def reset_theme(request):
    theme = ThemeSetting.get_solo()
    theme.palette = "aurora"
    theme.font_family = "Inter"
    theme.updated_by = request.user
    theme.save()
    messages.info(request, "Tema website dikembalikan ke pengaturan awal.")
    return redirect("theme_settings")


# Endpoint callback dari Google
@psa('social:complete')
def google_login(request):
    # token dari front-end (Google One Tap / button)
    token = request.POST.get('credential')
    if token:
        try:
            # authenticate user dengan token
            user = request.backend.do_auth(token)
            if user:
                login(request, user)
                return redirect('dashboard')
        except Exception as e:
            print("Login error:", e)
    return redirect('home')