from django.urls import path

from .views import CartView


urlpatterns = [
    path('cart/<int:pk>/', CartView.as_view(), name='cart'),
    path('cart/<int:cart_pk>/add/<int:product_pk>/',
         CartView.add_to_cart,
         name='add_to_cart'),
    path('cart/<int:cart_pk>/remove/<int:order_item_pk>/',
         CartView.remove_from_cart,
         name='remove_from_cart')
]
