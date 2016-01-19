from django import forms
from .models import Owner


class EditContactForm(forms.ModelForm):
    """Form for edit contact information page."""
    class Meta:
        model = Owner
