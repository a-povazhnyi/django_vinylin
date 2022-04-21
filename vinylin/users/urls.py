from django.urls import path, include

from .views import (sign_in, Register)

urlpatterns = [
    path('sign-in/', sign_in, name='sign-in'),
    path('register/', Register.as_view(), name='register'),
]
