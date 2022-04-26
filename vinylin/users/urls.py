from django.urls import path, include

from .views import (
    SignIn, SignOut, Register, SignExceptions,
    EmailVerification, EmailChange, EmailConfirm
)

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('register/', Register.as_view(), name='register'),
    path('sign-exceptions/', SignExceptions.as_view(), name='sign_exceptions'),

    path('email-verification/',
         EmailVerification.as_view(),
         name='email_verification'),
    path('email-confirm/<str:verification_code>/',
         EmailConfirm.as_view(),
         name='email_confirm'),
    path('email-change/',
         EmailChange.as_view(),
         name='email_change'),
]
