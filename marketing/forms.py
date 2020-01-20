from django import forms
from .models import Signup


class HomeEmailSignupForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "text",
        "name": "email",
        "placeholder": "Type your email address",
        "id": "email"
    }), label="")

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "name": "first_name",
        "placeholder": "Type your first name",
        "id": "first_name"
    }), label="")

    class Meta:
        model = Signup
        fields = ['email', 'first_name']
