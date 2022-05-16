from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F, DecimalField
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.shortcuts import redirect, render

from .forms import OrderItemQuantityForm
from .models import OrderItem, Order
from .utils import count_total_price
from store.models import Storage


class CartView(ListView):
    template_name = 'orders/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return OrderItem.objects.filter(cart_id=self.kwargs['pk'])\
            .order_by('product_id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_pk'] = self.kwargs['pk']
        context['total_price'] = self._count_total_price()
        return context

    def _count_total_price(self):
        order_items = self.get_queryset()
        return count_total_price(order_items)

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

    def remove_from_cart(self, cart_pk, order_item_pk):
        OrderItem.objects.get(pk=order_item_pk).delete()
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


class OrderView(ListView):
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        return super(OrderView, self).get_context_data(**kwargs)


class MakeOrderView(CreateView):
    def get(self, request, *args, **kwargs):
        return self._make_order(request, kwargs['cart_pk'])

    def _make_order(self, request, cart_pk):
        order_items = OrderItem.objects.filter(cart_id=cart_pk)
        total_price = count_total_price(order_items)

        with transaction.atomic():
            discard_balance_or_alert = self._discard_user_balance(
                request,
                total_price,
                cart_pk
            )
            if isinstance(discard_balance_or_alert, HttpResponse):
                return discard_balance_or_alert

            self._update_storage(order_items)
            new_order = Order.objects.create(
                user=request.user,
                status='PA',
                total_price=total_price,
            )
            order_items.update(order=new_order, cart=None)
            return redirect('orders')

    @staticmethod
    def _discard_user_balance(request, total_price, cart_pk):
        try:
            user_profile = request.user.profile
            new_user_balance = float(user_profile.balance) - total_price

            decimal = DecimalField(max_digits=6, decimal_places=2)
            new_user_balance = str(round(new_user_balance, 2))
            new_user_balance = decimal.clean(new_user_balance,
                                             model_instance=None)
            user_profile.balance = new_user_balance
            user_profile.save()

        except ValidationError:
            context = {
                'alert_message': ValidationError.messages,
                'redirect_url': reverse_lazy('cart',
                                             kwargs={'pk': cart_pk})
            }
            return render(request, 'alert.html', context)

    @staticmethod
    def _update_storage(queryset):
        """Update product storage quantities"""
        storage_objets = []
        for item in queryset:
            obj = Storage.objects.get(product=item.product)
            obj.quantity = F('quantity') - item.quantity
            storage_objets.append(obj)

        return Storage.objects.bulk_update(storage_objets, ['quantity'])
