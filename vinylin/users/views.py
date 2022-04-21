from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import login, logout

from .forms import UserForm


def sign_in(request):
    return render(request, 'users/signin.html')


class SignOut(TemplateView):
    template_name = 'vinyl/index.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['alert'] = 'You successfully signed out!'
        return context


class Register(CreateView):
    def get(self, request, *args, **kwargs):
        user_form = UserForm()
        context = {'user_form': user_form}
        return render(request, 'users/register.html', context)

    def post(self, request, *args, **kwargs):
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user)
            return redirect('https://www.google.com/')
