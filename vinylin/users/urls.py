from django.urls import path, include

from .views import (sign_in, SignOut, Register)

urlpatterns = [
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('register/', Register.as_view(), name='register'),
]
