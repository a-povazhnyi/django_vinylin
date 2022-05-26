from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth import forms as auth_forms
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

from .models import Profile
from vinyl.models import Country


UserModel = get_user_model()


class SignInForm(auth_forms.AuthenticationForm):
    username = forms.CharField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'input-default',
            'placeholder': 'email'
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'input-default',
            'placeholder': 'password',
        })
    )


class UserForm(auth_forms.UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input-default',
            'placeholder': 'password',
        }),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password',
            'class': 'input-default',
            'placeholder': 'password',
        }),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    phone = PhoneNumberField(
        required=False,
        widget=PhoneNumberInternationalFallbackWidget(attrs={
            'class': 'input-default',
            'placeholder': 'phone',
        })
    )
    birthday = forms.DateField(
        required=False,
        label=_('Birthday'),
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'input-default'}
        )
    )
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password1"))

        if commit:
            user.save()
            if not self._is_profile_blank():
                profile = Profile.objects.get(user=user.pk)
                self._save_profile(profile=profile)
        return user

    def _is_profile_blank(self):
        for field in ('phone', 'birthday', 'country'):
            if field in self.changed_data:
                return False
        return True

    def _get_profile_data(self):
        phone = self.cleaned_data.get('phone')

        profile_data = {
            'phone': phone,
            'birthday': self.cleaned_data.get('birthday'),
            'country': self.cleaned_data.get('country'),
        }
        return profile_data

    def _save_profile(self, profile: Profile):
        profile_data = self._get_profile_data()
        profile.phone = profile_data.get('phone')
        profile.birthday = profile_data.get('birthday')
        profile.country_id = profile_data.get('country')

        profile.save()
        return profile

    class Meta:
        model = UserModel
        fields = ('email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'input-default',
                'placeholder': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-default',
                'placeholder': '@mail'}),
            'first_name': forms.TextInput(attrs={
                'class': 'input-default',
                'placeholder': 'first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-default',
                'placeholder': 'last name'
            }),
        }


class TokenForm(forms.Form):
    code = forms.CharField(
        label='Your code:',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-default',
            'placeholder': 'past your code here ...'
        })
    )


class EmailForm(forms.Form):
    new_email = forms.EmailField(
        label='New e-mail address:',
        widget=forms.EmailInput(attrs={
            'class': 'input-default',
            'placeholder': 'enter your new e-mail ...'
        })
    )


class AddBalanceAdminForm(forms.Form):
    balance = forms.IntegerField(
        label=_('Balance will increase by this number'),
        widget=forms.NumberInput(),
        validators=[MinValueValidator(0)]
    )
