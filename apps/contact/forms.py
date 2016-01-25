from django import forms
from .models import Owner


class EditContactForm(forms.ModelForm):
    """Form for edit contact information page."""
    def __init__(self, *args, **kwargs):
        super(EditContactForm, self).__init__(*args, **kwargs)
        # init style class for form fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Owner
