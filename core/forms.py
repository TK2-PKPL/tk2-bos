from django import forms
from .models import FONT_CHOICES, PALETTE_CHOICES


class ThemeForm(forms.Form):
    palette = forms.ChoiceField(choices=PALETTE_CHOICES, widget=forms.RadioSelect)
    font_family = forms.ChoiceField(choices=FONT_CHOICES, widget=forms.RadioSelect)
