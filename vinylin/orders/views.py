from django.db.models import F
from django.views.generic import ListView
from django.shortcuts import redirect

from .forms import OrderItemQuantityForm
from .models import OrderItem


class CartView(ListView):
    template_name = 'orders/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return OrderItem.objects.filter(cart_id=self.kwargs['pk'])\
            .order_by('product_id')

    def add_to_cart(self, cart_pk, product_pk):
        order_item, created_order_item = OrderItem.objects.get_or_create(
            cart_id=cart_pk,
            order=None,
            product_id=product_pk,
        )
        if order_item and not created_order_item:
            order_item.quantity = F('quantity') + 1
            order_item.save()

        return redirect('cart', pk=cart_pk)

    def post(self, request, *args, **kwargs):
        order_item_id = int(request.POST['order_item_id'])
        order_item_obj = OrderItem.objects.get(pk=order_item_id)
        form = OrderItemQuantityForm(
            data=request.POST,
            instance=order_item_obj
        )

        if not form.is_valid():
            return redirect('cart', pk=request.user.cart.pk)

        form.save()
        return redirect('cart', pk=request.user.cart.pk)
