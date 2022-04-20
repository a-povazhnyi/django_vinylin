from django.shortcuts import render


def sign_in(request):
    return render(request, 'users/signin.html')


def register(request):
    return render(request, 'users/register.html')
