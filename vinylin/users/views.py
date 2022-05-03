from django.shortcuts import render, redirect
from django.views.generic import (
    UpdateView,
    CreateView,
    TemplateView,
    DetailView,
)
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

from .models import Profile
from .forms import SignInForm, UserForm, ProfileForm, TokenForm, EmailForm
from .decorators import anonymous_only
from .tokens import TokenGenerator
from .emails import EmailConfirmMessage
from .mixins import SignRequiredMixin


UserModel = auth_views.get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'users/sign_in.html'
    form_class = SignInForm
    redirect_field_name = ''

    @anonymous_only(redirect_url='sign_exceptions')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, *kwargs)


class SignOutView(SignRequiredMixin, auth_views.LogoutView):
    template_name = 'users/sign_out.html'
    extra_context = {'redirect_url': '/'}


class RegisterView(CreateView):
    @anonymous_only(redirect_url='sign_exceptions')
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        context = {'user_form': user_form}
        return render(request, 'users/register.html', context)

    @anonymous_only(redirect_url='sign_exceptions')
    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)

        if not user_form.is_valid():
            context = {'user_form': user_form}
            return render(request, 'users/register.html', context)

        new_user = user_form.save()
        login(request, new_user)
        return redirect('email_verification')


class ProfileView(DetailView):
    template_name = 'users/profile.html'

    def get_queryset(self):
        user_pk = self.request.user.pk
        return UserModel.objects\
            .select_related('profile')\
            .select_related('profile__country')\
            .filter(pk=user_pk)

    def get(self, request, *args, **kwargs):
        if request.user.pk == kwargs['pk']:
            return super().get(request, *args, **kwargs)

        context = {
            'alert_message': ('You have not enough permissions '
                              'to see this page'),
            'redirect_url': '/'
        }
        return render(request, 'alert.html', context)


class SignExceptionsView(TemplateView):
    template_name = 'alert.html'
    extra_context = {
        'redirect_url': '/',
        'alert_message': 'This page is not accessible to authorized users!'
    }


class EmailVerificationView(SignRequiredMixin, TemplateView):
    template_name = 'users/email_verification.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token_generator = TokenGenerator()

    def get(self, request, *args, **kwargs):
        if self._db_email_confirmed(request):
            context = {'email_confirmed': True}
            return render(request, 'users/email_verification.html', context)

        token_form = TokenForm()
        context = {'token_form': token_form}
        return render(request, 'users/email_verification.html', context)

    def post(self, request, *args, **kwargs):
        token_form = TokenForm(data=request.POST)

        if not token_form.changed_data and token_form.is_valid():
            code = self._make_token(request)
            self._mail_code(request, code)

            context = {'token_form': token_form, 'is_sent': True}
            return render(request, 'users/email_verification.html', context)

        user_token = token_form.data.get('code')
        if not user_token or not token_form.is_valid():
            context = {'token_form': token_form, 'is_sent': False}
            return render(request, 'users/email_verification.html', context)

        return redirect(f'/users/email-confirm/{user_token}/',
                        user_code=user_token)

    def _make_token(self, request):
        new_token = self._token_generator.make_token(request.user)
        return new_token

    @staticmethod
    def _db_email_confirmed(request):
        if UserModel.objects.get(pk=request.user.pk).is_email_verified:
            return True

    @staticmethod
    def _mail_code(request, code):
        email_to = request.user.email
        email_confirm = EmailConfirmMessage(code=code, to=[email_to])
        email_confirm.send(fail_silently=True)


class EmailConfirmView(SignRequiredMixin, TemplateView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._token_generator = TokenGenerator()

    def get(self, request, *args, **kwargs):
        user = request.user
        user_token = kwargs.get('token')
        user_token_checked = self._token_generator.check_token(
            user=user,
            token=user_token
        )

        if not user_token or not user_token_checked:
            context = {'email_confirmed': False}
            return render(request, 'users/email_confirmed.html', context)

        user.is_email_verified = True
        user.save()

        context = {'email_confirmed': True}
        return render(request, 'users/email_confirmed.html', context)


class EmailChangeView(SignRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        email_form = EmailForm()
        context = {
            'email_form': email_form,
            'current_email': request.user.email,
        }
        return render(request, 'users/email_change.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        email_form = EmailForm(data=request.POST)
        new_email = email_form.data.get('new_email')

        if not new_email or not email_form.is_valid():
            context = {
                'email_form': email_form,
                'current_email': user.email,
            }
            return render(request, 'users/email_change.html', context)

        user.email = new_email
        user.is_email_verified = False
        user.save()
        return redirect('email_verification')


class PasswordChangeView(SignRequiredMixin, auth_views.PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'users/password_change.html'

    def get_success_url(self, *args, **kwargs):
        return reverse('password_alert')


class PasswordChangeCompleteView(TemplateView):
    template_name = 'alert.html'
    extra_context = {
        'redirect_url': '/',
        'alert_message': 'Your password is changed successfully!',
    }


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'users/password_reset.html'
    token_generator = TokenGenerator()
    email_template_name = 'users/password_reset_email.html'


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    """
    The page shown after a user has been emailed a link
    to reset their password.
    """
    template_name = 'alert.html'
    extra_context = {
        'redirect_url': '/',
        'alert_message': 'Check your e-mail to reset the password...'
    }


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    """Presents a form for entering a new password"""
    template_name = 'users/password_confirm.html'
    token_generator = TokenGenerator()


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    """
    Presents a view which informs the user that
    the password has been successfully changed.
    """
    template_name = 'alert.html'
    extra_context = {
        'redirect_url': '/users/sign-in/',
        'alert_message': 'Your password has been changed. Sign in!',
    }
