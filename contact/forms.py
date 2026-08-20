from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="")

    class Meta:
        model = ContactMessage
        fields = ("name", "email", "phone", "company", "project_type", "budget", "message")
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_message(self):
        value = self.cleaned_data["message"].strip()
        if len(value) < 20:
            raise forms.ValidationError("Please add a little more detail.")
        return value
