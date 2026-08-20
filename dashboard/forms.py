from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StaffAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        super().confirm_login_allowed(user)
        if not user.is_staff:
            raise forms.ValidationError("This account does not have dashboard access.", code="not_staff")


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ProjectGalleryUploadForm(forms.Form):
    images = forms.FileField(widget=MultiFileInput(attrs={"accept": "image/*", "multiple": True}))
