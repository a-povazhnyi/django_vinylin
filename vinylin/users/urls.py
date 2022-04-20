from django.urls import path, include

from . import views

urlpatterns = [
    path('sign-in/', views.sign_in, name='sign-in'),
    path('register/', views.register, name='register'),
]