from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F, DecimalField, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import redirect, render

from .emails import AddCartItemEmailMessage, OrderEmailMessage
from .forms import OrderItemQuantityForm
from .models import OrderItem, Order
from .mixins import UserOrdersPermissionMixin
from store.models import Storage


class CartView(UserOrdersPermissionMixin, ListView):
    template_name = 'orders/cart.html'
    context_object_name = 'cart_items'

    def get_queryset(self):
        return (
            OrderItem.objects.filter(cart_id=self.kwargs.get('cart_pk'))
                             .order_by('product_id')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_pk'] = self.kwargs.get('cart_pk')
        context['total_price'] = count_total_price(self.get_queryset())
        return context

    def post(self, request, *args, **kwargs):
        """Used to change the quantity of order items in the cart"""
        order_item_id = request.POST['order_item_id']
        order_item_obj = OrderItem.objects.get(pk=order_item_id)
        form = OrderItemQuantityForm(
            data=request.POST,
            instance=order_item_obj
        )

        if not form.is_valid():
            return redirect('cart', cart_pk=request.user.cart.pk)

        form.save()
        return redirect('cart', cart_pk=request.user.cart.pk)


class AddCartItemView(UserOrdersPermissionMixin, CreateView):
    model = OrderItem

    def get(self, request, *args, **kwargs):
        return self._add_to_cart(request, *args, **kwargs)

    @staticmethod
    def _add_to_cart(request, *args, **kwargs):
        cart_pk = kwargs.get('cart_pk')
        product_pk = kwargs.get('product_pk')

        order_item, created_order_item = OrderItem.objects.get_or_create(
            cart_id=cart_pk,
            order=None,
            product_id=product_pk,
        )
        if not created_order_item:
            order_item.quantity = F('quantity') + 1
            order_item.save()

        # if request.user.is_email_verified:
        # self._mail_order_item(request, {'item': order_item})
        return redirect('cart', cart_pk=cart_pk)

    @staticmethod
    def _mail_order_item(request, context):
        message = AddCartItemEmailMessage(request, context)
        return message.send(fail_silently=True)


class RemoveCartItemView(UserOrdersPermissionMixin, UpdateView):
    model = OrderItem

    def get(self, request, *args, **kwargs):
        order_item_pk = kwargs.get('order_item_pk')
        cart_pk = kwargs.get('cart_pk')
        OrderItem.objects.filter(pk=order_item_pk).delete()
        return redirect('cart', cart_pk=cart_pk)


class OrderView(ListView):
    template_name = 'orders/orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return (
            Order.objects.filter(user=self.request.user)
                         .prefetch_related('order_items')
        )


class MakeOrderView(UserOrdersPermissionMixin, CreateView):
    def get(self, request, *args, **kwargs):
        return self._make_order(request, kwargs.get('cart_pk'))

    @transaction.atomic
    def _make_order(self, request, cart_pk):
        order_items = OrderItem.objects.filter(cart_id=cart_pk)
        total_price = count_total_price(order_items)

        discard_balance = self._discard_user_balance(request, total_price)
        if not discard_balance:
            return self._alert_user(request, cart_pk)

        self._update_storage(order_items)
        new_order = Order.objects.create(
            user=request.user,
            status='PA',
            total_price=total_price,
        )
        order_items.update(order=new_order, cart=None)

        context = {
            'order_items': OrderItem.objects.filter(order=new_order),
            'total_price': total_price,
        }
        self._mail_order(request, context)
        return redirect('orders')

    @staticmethod
    def _discard_user_balance(request, total_price):
        try:
            user_profile = request.user.profile
            new_user_balance = float(user_profile.balance) - float(total_price)

            decimal = DecimalField(max_digits=6, decimal_places=2)
            new_user_balance = str(round(new_user_balance, 2))
            new_user_balance = decimal.clean(new_user_balance,
                                             model_instance=None)
            user_profile.balance = new_user_balance
            user_profile.save()
            return user_profile

        except ValidationError:
            return None

    @staticmethod
    def _alert_user(request, cart_pk):
        context = {
            'alert_message': 'You have not enough balance to make this order',
            'redirect_url': reverse_lazy('cart',
                                         kwargs={'cart_pk': cart_pk})
        }
        return render(request, 'alert.html', context)

    @staticmethod
    def _update_storage(queryset):
        """Updates the quantity of products in the storage"""
        storages = []
        for item in queryset.select_related('product__storage'):
            storage = item.product.storage
            storage.quantity = F('quantity') - item.quantity
            storages.append(storage)

        return Storage.objects.bulk_update(storages, ['quantity'])

    @staticmethod
    def _mail_order(request, context):
        message = OrderEmailMessage(request, context)
        return message.send(fail_silently=True)


def count_total_price(queryset):
    if not queryset.exists():
        return None
    return round(queryset.aggregate(Sum('final_price'))['final_price__sum'], 2)
