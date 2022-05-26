from django.urls import path

from .views import (
    CartView,
    AddCartItemView,
    RemoveCartItemView,
    MakeOrderView,
    OrderView,
)


urlpatterns = [
    path('cart/<int:cart_pk>/', CartView.as_view(), name='cart'),
    path('cart/<int:cart_pk>/add/<int:product_pk>/',
         AddCartItemView.as_view(),
         name='add_to_cart'),
    path('cart/<int:cart_pk>/remove/<int:order_item_pk>/',
         RemoveCartItemView.as_view(),
         name='remove_from_cart'),

    path('make-order/<int:cart_pk>/',
         MakeOrderView.as_view(),
         name='make_order'),
    path('', OrderView.as_view(), name='orders'),
]
