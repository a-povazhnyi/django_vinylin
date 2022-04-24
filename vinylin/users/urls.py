from django.urls import path, include

from .views import (SignIn, SignOut, Register, SignExceptions)

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('register/', Register.as_view(), name='register'),
    path('sign-exceptions/', SignExceptions.as_view(), name='sign_exceptions'),
]
