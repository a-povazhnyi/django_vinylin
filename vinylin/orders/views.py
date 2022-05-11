from django.db.models import F
from django.views.generic import DetailView
from django.shortcuts import redirect

from .models import Cart, OrderItem


class CartView(DetailView):
    template_name = 'orders/cart.html'

    def get_queryset(self):
        return Cart.objects.filter(pk=self.kwargs['pk'])

    def add_to_cart(self, cart_pk, product_pk):
        order_item, created_order_item = OrderItem.objects.get_or_create(
            cart_id=cart_pk,
            order=None,
            product_id=product_pk,
        )
        if order_item:
            order_item.quantity = F('quantity') + 1
            order_item.save()
        return redirect('vinyl_single', pk=product_pk)
