from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth import forms as auth_forms
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Profile

UserModel = get_user_model()


class SignInForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'input1',
            'placeholder': 'email'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'input1',
            'placeholder': 'password',
        })
    )


class UserForm(auth_forms.UserCreationForm):
    class Meta:
        model = UserModel
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


class ProfileForm(forms.ModelForm):
    phone = PhoneNumberField(
        required=False,
        widget=PhoneNumberInternationalFallbackWidget(attrs={
            'class': 'input1',
            'placeholder': 'phone',
        })
    )

    class Meta:
        model = Profile
        fields = ('phone', 'birthday', 'country')
        widgets = {
            'age': forms.NumberInput(attrs={
                'class': 'input1',
                'placeholder': 'age',
                'min': '0',
                'max': '170',
            }),
        }


class TokenForm(forms.Form):
    code = forms.CharField(
        label='Your code:',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input1',
            'placeholder': 'past your code here ...'
        })
    )


class EmailForm(forms.Form):
    new_email = forms.EmailField(
        label='New e-mail address:',
        widget=forms.EmailInput(attrs={
            'class': 'input1',
            'placeholder': 'enter your new e-mail ...'
        })
    )
