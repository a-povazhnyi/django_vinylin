from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import Profile


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input1',
                'placeholder': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input1',
                'placeholder': '@mail'}),
            'first_name': forms.TextInput(attrs={
                'class': 'input1',
                'placeholder': 'first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input1',
                'placeholder': 'last name'
            }),
        }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input1',
            'placeholder': 'password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input1',
            'placeholder': 'password',
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
