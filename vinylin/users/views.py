from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login

from .models import Profile
from .forms import SignInForm, UserForm, ProfileForm


class SignIn(auth_views.LoginView):
    template_name = 'users/signin.html'
    form_class = SignInForm


class SignOut(auth_views.LogoutView):
    template_name = 'users/signout.html'
    extra_context = {'redirect_url': '/'}


class Register(CreateView):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        profile_form = ProfileForm()
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'users/register.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()

            # Checks if profile form is not blank
            if profile_form.changed_data:
                new_profile = Profile.objects.get(user_id=new_user.pk)
                new_profile_form = ProfileForm(data=request.POST,
                                               instance=new_profile)
                new_profile_form.save()

            login(request, new_user)
            return redirect('index')

        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(request, 'users/register.html', context)


class SignExceptions(TemplateView):
    template_name = 'users/sign_exceptions.html'
    extra_context = {'redirect_url': '/'}
