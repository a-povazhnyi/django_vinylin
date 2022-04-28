from django.shortcuts import render, redirect
from django.views.generic import (
    UpdateView, CreateView, TemplateView, DetailView
)
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse

from .models import Profile
from .forms import SignInForm, UserForm, ProfileForm, TokenForm, EmailForm
from .decorators import anonymous_required
from .tokens import TokenGenerator
from .backends import EmailConfirmMessage
from .mixins import SignRequiredMixin


UserModel = auth_views.get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'users/sign_in.html'
    form_class = SignInForm
    redirect_field_name = ''

    @anonymous_required(redirect_url='sign_exceptions')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, *kwargs)


class SignOutView(SignRequiredMixin, auth_views.LogoutView):
    template_name = 'users/sign_out.html'
    extra_context = {'redirect_url': '/'}


class RegisterView(CreateView):
    @anonymous_required(redirect_url='sign_exceptions')
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = ProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'users/register.html', context)

    @anonymous_required(redirect_url='sign_exceptions')
    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()

            # Checks if profile form is not blank
            if profile_form.changed_data:
                new_profile = Profile.objects.get(user=new_user.pk)
                new_profile_form = ProfileForm(data=request.POST,
                                               instance=new_profile)
                new_profile_form.save()

            login(request, new_user)
            return redirect('email_verification')

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'users/register.html', context)


class SignExceptionsView(TemplateView):
    template_name = 'alert.html'
    extra_context = {
        'redirect_url': '/',
        'alert_message': 'This page is not accessible to authorized users!'
    }


class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = UserModel

    def get(self, request, *args, **kwargs):
        user_pk = request.user.pk
        if user_pk == kwargs['pk']:
            return super().get(request, *args, **kwargs)

        alert_message = 'You have not enough permissions see to this page'
        context = {
            'alert_message': alert_message,
            'redirect_url': '/'
        }
        return render(request, 'alert.html', context)


class EmailVerificationView(SignRequiredMixin, TemplateView):
    template_name = 'users/email_verification.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = TokenGenerator()

    def get(self, request, *args, **kwargs):
        if self._db_email_confirmed(request):
            context = {'email_confirmed': True}
            return render(request, 'users/email_verification.html', context)

        code_form = TokenForm()
        context = {'code_form': code_form}
        return render(request, 'users/email_verification.html', context)

    def post(self, request, *args, **kwargs):
        code_form = TokenForm(data=request.POST)

        if not code_form.changed_data and code_form.is_valid():
            code = self._make_token(request)
            self._mail_code(request, code)

            context = {'code_form': code_form, 'is_sent': True}
            return render(request, 'users/email_verification.html', context)

        user_code = code_form.data.get('code')
        if user_code and code_form.is_valid():
            return redirect(f'/users/email-confirm/{user_code}/',
                            user_code=user_code)

        context = {'code_form': code_form, 'is_sent': False}
        return render(request, 'users/email_verification.html', context)

    def _make_token(self, request):
        new_token = self.token.make_token(request.user)
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
        self.token = TokenGenerator()

    def get(self, request, *args, **kwargs):
        user_id = request.user.pk
        user_code = kwargs.get('verification_code')

        if user_code and self.token.check_token(request.user, user_code):
            user = UserModel.objects.get(pk=user_id)
            user.is_email_verified = True
            user.save()

            context = {'email_confirmed': True}
            return render(request, 'users/email_confirmed.html', context)

        context = {'email_confirmed': False}
        return render(request, 'users/email_confirmed.html', context)


class EmailChangeView(SignRequiredMixin, UpdateView):
    def get(self, request, *args, **kwargs):
        email_form = EmailForm()
        user_email = UserModel.objects.get(pk=request.user.pk).email

        context = {'email_form': email_form, 'current_email': user_email}
        return render(request, 'users/email_change.html', context)

    def post(self, request, *args, **kwargs):
        user = UserModel.objects.get(pk=request.user.pk)
        current_email = user.email

        email_form = EmailForm(data=request.POST)
        new_email = email_form.data.get('new_email')

        if email_form.is_valid() and new_email:
            user.email = new_email
            user.is_email_verified = False
            user.save()
            return redirect('email_verification')

        context = {'email_form': email_form, 'current_email': current_email}
        return render(request, 'users/email_change.html', context)


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
