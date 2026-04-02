import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from core.models import AuditLog
from core.utils import get_client_ip

User = get_user_model()


def build_unique_username(email: str) -> str:
    base = email.split("@")[0].strip().lower()
    safe_base = (
        base.replace(".", "_")
        .replace("+", "_")
        .replace("-", "_")
        .replace(" ", "_")
    ) or "user"

    username = safe_base
    counter = 1

    while User.objects.exclude(email=email).filter(username=username).exists():
        username = f"{safe_base}_{counter}"
        counter += 1

    return username


def _extract_google_credential(request):
    credential = None

    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8"))
            credential = payload.get("credential")
        except json.JSONDecodeError:
            credential = None
    else:
        credential = request.POST.get("credential")

    return credential


def _verify_and_login(request, credential):
    if not credential:
        return {
            "ok": False,
            "message": "Credential Google tidak ditemukan.",
            "status": 400,
        }

    if not settings.GOOGLE_CLIENT_ID:
        return {
            "ok": False,
            "message": "GOOGLE_CLIENT_ID belum diisi di file .env.",
            "status": 400,
        }

    try:
        token_info = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
    except Exception:
        return {
            "ok": False,
            "message": "Token Google gagal diverifikasi.",
            "status": 400,
        }

    issuer = token_info.get("iss")
    if issuer not in {"accounts.google.com", "https://accounts.google.com"}:
        return {
            "ok": False,
            "message": "Issuer token Google tidak valid.",
            "status": 400,
        }

    if not token_info.get("email_verified", False):
        return {
            "ok": False,
            "message": "Email Google belum terverifikasi.",
            "status": 400,
        }

    email = token_info.get("email", "").strip().lower()
    sub = token_info.get("sub", "").strip()

    if not email or not sub:
        return {
            "ok": False,
            "message": "Data akun Google tidak lengkap.",
            "status": 400,
        }

    role = User.ROLE_EDITOR if email in settings.TEAM_EDITOR_EMAILS else User.ROLE_VIEWER

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": build_unique_username(email),
            "first_name": token_info.get("given_name", "").strip(),
            "last_name": token_info.get("family_name", "").strip(),
            "display_name": token_info.get("name", "").strip() or email.split("@")[0],
            "google_sub": sub,
            "avatar_url": token_info.get("picture", "").strip(),
            "role": role,
        },
    )

    if created:
        user.set_unusable_password()

    user.google_sub = sub
    user.avatar_url = token_info.get("picture", "").strip()
    user.first_name = token_info.get("given_name", "").strip()
    user.last_name = token_info.get("family_name", "").strip()
    user.display_name = token_info.get("name", "").strip() or user.display_name or user.username
    user.role = role
    user.save()

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    AuditLog.objects.create(
        actor=user,
        action="google_login",
        detail=f"Login Google berhasil. Role: {user.role}",
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
    )

    messages.success(request, f"Selamat datang, {user.display_name}.")

    return {
        "ok": True,
        "redirect": reverse("dashboard"),
        "role": user.role,
        "status": 200,
    }


@csrf_exempt
@require_http_methods(["GET", "POST"])
def google_login(request):
    if request.method == "GET":
        return redirect("home")

    credential = _extract_google_credential(request)
    result = _verify_and_login(request, credential)

    wants_json = request.content_type and "application/json" in request.content_type

    if wants_json:
        status_code = result.pop("status", 200)
        return JsonResponse(result, status=status_code)

    if result.get("ok"):
        return redirect(result["redirect"])

    messages.error(request, result.get("message", "Login Google gagal diproses."))
    return redirect("home")


@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(
            actor=request.user,
            action="logout",
            detail="Pengguna keluar dari sistem.",
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
        )

    logout(request)
    messages.info(request, "Anda sudah logout.")
    return redirect("home")


@require_POST
def debug_login(request, role):
    if not settings.DEBUG:
        return JsonResponse({"ok": False, "message": "Not found."}, status=404)

    role = role.strip().lower()
    if role not in {User.ROLE_EDITOR, User.ROLE_VIEWER}:
        return JsonResponse({"ok": False, "message": "Role tidak valid."}, status=400)

    email = f"demo_{role}@example.com"
    display_name = f"Demo {role.title()}"

    user, _ = User.objects.get_or_create(
        email=email,
        defaults={
            "username": f"demo_{role}",
            "display_name": display_name,
            "role": role,
        },
    )

    user.role = role
    user.display_name = display_name
    user.set_unusable_password()
    user.save()

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    AuditLog.objects.create(
        actor=user,
        action="debug_login",
        detail=f"Masuk menggunakan akun debug {role}.",
        ip_address=get_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
    )

    return JsonResponse(
        {
            "ok": True,
            "redirect": reverse("dashboard"),
        }
    )