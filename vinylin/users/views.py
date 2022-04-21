from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth import login

from .forms import UserForm


def sign_in(request):
    return render(request, 'users/signin.html')


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
