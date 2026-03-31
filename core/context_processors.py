from django.conf import settings
from .models import ThemeSetting
from .team_data import SITE_NAME, SITE_TAGLINE, PROJECT_CONTEXT, TEAM_MEMBERS, FEATURE_CARDS, TASK_ONE_HIGHLIGHTS, AUTHORIZATION_RULES

PALETTE_MAP = {
    "aurora": {"name": "Aurora Blue", "primary": "#2f6bff", "secondary": "#8fc7ff", "accent": "#edf5ff", "surface": "#ffffff", "surface_soft": "#f4f8ff", "text": "#12233f", "muted": "#56708f", "ring": "rgba(47, 107, 255, 0.18)"},
    "emerald": {"name": "Emerald Calm", "primary": "#1d8f6c", "secondary": "#7dd6ba", "accent": "#edf9f5", "surface": "#ffffff", "surface_soft": "#f3fbf8", "text": "#17332d", "muted": "#4b6d63", "ring": "rgba(29, 143, 108, 0.18)"},
    "sunset": {"name": "Sunset Coral", "primary": "#dc5c4c", "secondary": "#f4ae9d", "accent": "#fff2ef", "surface": "#ffffff", "surface_soft": "#fff7f5", "text": "#3b241f", "muted": "#7f625c", "ring": "rgba(220, 92, 76, 0.18)"},
    "midnight": {"name": "Midnight Plum", "primary": "#5a46cc", "secondary": "#b8adff", "accent": "#f3f1ff", "surface": "#ffffff", "surface_soft": "#f8f7ff", "text": "#221b4c", "muted": "#61598a", "ring": "rgba(90, 70, 204, 0.18)"},
}
FONT_MAP = {"Inter": '"Inter", "Segoe UI", sans-serif', "Poppins": '"Poppins", "Segoe UI", sans-serif', "Lora": '"Lora", Georgia, serif', "Space Grotesk": '"Space Grotesk", "Segoe UI", sans-serif'}

def site_context(request):
    theme = ThemeSetting.get_solo()
    return {
        "site_name": SITE_NAME,
        "site_tagline": SITE_TAGLINE,
        "project_context": PROJECT_CONTEXT,
        "team_members": TEAM_MEMBERS,
        "feature_cards": FEATURE_CARDS,
        "task_one_highlights": TASK_ONE_HIGHLIGHTS,
        "authorization_rules": AUTHORIZATION_RULES,
        "active_theme": theme,
        "palette_tokens": PALETTE_MAP.get(theme.palette, PALETTE_MAP["aurora"]),
        "font_css_stack": FONT_MAP.get(theme.font_family, FONT_MAP["Inter"]),
        "google_client_id": settings.GOOGLE_CLIENT_ID,
        "debug_mode": settings.DEBUG,
    }
