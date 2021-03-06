from django.urls import path

from .views import IndexView, VinylDetailView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('<int:pk>/', VinylDetailView.as_view(), name='vinyl_single'),
]
