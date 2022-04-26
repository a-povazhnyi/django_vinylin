from django.urls import path

from .views import (
    SignIn, SignOut, Register, SignExceptionsView,
    EmailVerification, EmailChange, EmailConfirm,
    PasswordChangeView, PasswordResetView, PasswordAlertView,
)

urlpatterns = [
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('register/', Register.as_view(), name='register'),
    path('sign-exceptions/',
         SignExceptionsView.as_view(),
         name='sign_exceptions'),

    path('email-verification/',
         EmailVerification.as_view(),
         name='email_verification'),
    path('email-confirm/<str:verification_code>/',
         EmailConfirm.as_view(),
         name='email_confirm'),
    path('email-change/',
         EmailChange.as_view(),
         name='email_change'),

    path('password-change/',
         PasswordChangeView.as_view(),
         name='password_change'),
    path('password-reset/',
         PasswordResetView.as_view(),
         name='password_reset'),
    path('password-alert/',
         PasswordAlertView.as_view(),
         name='password_alert'),
]
