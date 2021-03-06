from django.urls import path

from .views import (
    SignInView,
    SignOutView,
    RegisterView,
    SignExceptionsView,
    ProfileView,
    EmailVerificationView,
    EmailChangeView,
    EmailConfirmView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordChangeCompleteView,
    PasswordResetCompleteView,
)


urlpatterns = [
    path('sign-in/', SignInView.as_view(), name='sign_in'),
    path('sign-out/', SignOutView.as_view(), name='sign_out'),
    path('register/', RegisterView.as_view(), name='register'),
    path('<int:pk>/', ProfileView.as_view(), name='profile'),
    path('sign-exceptions/',
         SignExceptionsView.as_view(),
         name='sign_exceptions'),

    path('email-verification/',
         EmailVerificationView.as_view(),
         name='email_verification'),
    path('email-confirm/<str:token>/',
         EmailConfirmView.as_view(),
         name='email_confirm'),
    path('email-change/',
         EmailChangeView.as_view(),
         name='email_change'),

    path('password-change/',
         PasswordChangeView.as_view(),
         name='password_change'),
    path('password-reset/',
         PasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('password-alert/',
         PasswordChangeCompleteView.as_view(),
         name='password_alert'),
]
