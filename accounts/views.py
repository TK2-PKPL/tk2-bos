import json
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from core.models import AuditLog
from core.utils import get_client_ip

User = get_user_model()

@require_POST
def google_login(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "message": "Permintaan login tidak valid."}, status=400)
    credential = payload.get("credential")
    if not credential:
        return JsonResponse({"ok": False, "message": "Token Google tidak ditemukan."}, status=400)
    if not settings.GOOGLE_CLIENT_ID:
        return JsonResponse({"ok": False, "message": "GOOGLE_CLIENT_ID belum diisi pada file env."}, status=400)
    try:
        token_info = id_token.verify_oauth2_token(credential, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
    except ValueError:
        return JsonResponse({"ok": False, "message": "Token Google tidak dapat diverifikasi."}, status=400)
    email = token_info.get("email", "").lower().strip()
    sub = token_info.get("sub")
    if not email or not sub:
        return JsonResponse({"ok": False, "message": "Data akun Google tidak lengkap."}, status=400)
    username_base = email.split("@")[0].replace(".", "_")
    username = username_base
    suffix = 1
    while User.objects.exclude(email=email).filter(username=username).exists():
        username = f"{username_base}_{suffix}"
        suffix += 1
    user, created = User.objects.get_or_create(email=email, defaults={
        "username": username,
        "first_name": token_info.get("given_name", ""),
        "last_name": token_info.get("family_name", ""),
        "display_name": token_info.get("name", username_base),
        "google_sub": sub,
        "avatar_url": token_info.get("picture", ""),
        "role": User.ROLE_EDITOR if email in settings.TEAM_EDITOR_EMAILS else User.ROLE_VIEWER,
    })
    if created:
        user.set_unusable_password()
    user.google_sub = sub
    user.avatar_url = token_info.get("picture", "")
    user.first_name = token_info.get("given_name", "")
    user.last_name = token_info.get("family_name", "")
    user.display_name = token_info.get("name", user.display_name or user.username)
    user.role = User.ROLE_EDITOR if email in settings.TEAM_EDITOR_EMAILS else User.ROLE_VIEWER
    user.save()
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    AuditLog.objects.create(actor=user, action="google_login", detail=f"Login Google berhasil dengan role {user.role}", ip_address=get_client_ip(request), user_agent=request.META.get("HTTP_USER_AGENT", "")[:255])
    messages.success(request, f"Selamat datang {user.display_name}.")
    return JsonResponse({"ok": True, "redirect": "/dashboard/"})

@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(actor=request.user, action="logout", detail="Pengguna keluar dari sesi aplikasi", ip_address=get_client_ip(request), user_agent=request.META.get("HTTP_USER_AGENT", "")[:255])
    logout(request)
    messages.info(request, "Anda telah keluar dari sesi aplikasi.")
    return redirect("home")

def debug_login(request, role):
    if not settings.DEBUG:
        return JsonResponse({"ok": False}, status=404)
    role = role.lower().strip()
    if role not in {User.ROLE_EDITOR, User.ROLE_VIEWER}:
        return JsonResponse({"ok": False}, status=400)
    email = f"demo_{role}@example.com"
    username = f"demo_{role}"
    user, _ = User.objects.get_or_create(email=email, defaults={"username": username, "display_name": f"Demo {role.title()}", "role": role})
    user.role = role
    user.set_unusable_password()
    user.save()
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    next_url = request.GET.get("next") or "/dashboard/"
    if request.method == "GET":
        return redirect(next_url)
    return JsonResponse({"ok": True, "redirect": next_url})
