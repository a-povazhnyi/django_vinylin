from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout

from .forms import SignInForm, RegisterForm


class SignIn(auth_views.LoginView):
    template_name = 'users/signin.html'
    form_class = SignInForm


class SignOut(auth_views.LogoutView):
    template_name = 'vinyl/index.html'


class Register(CreateView):
    def get(self, request, *args, **kwargs):
        register_form = RegisterForm()
        context = {'register_form': register_form}
        return render(request, 'users/register.html', context)

    def post(self, request, *args, **kwargs):
        register_form = RegisterForm(data=request.POST)

        if register_form.is_valid():
            new_user = register_form.save()
            login(request, new_user)
            return redirect('https://www.google.com/')
