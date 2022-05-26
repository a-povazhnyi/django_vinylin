from django import template

from orders.forms import OrderItemQuantityForm


register = template.Library()


@register.inclusion_tag('orders/cart_item_quantity.html')
def show_quantity_form(order_item_obj):
    form = OrderItemQuantityForm(
        initial={'quantity': order_item_obj.quantity},
        instance=order_item_obj,
    )
    context = {
        'form': form,
        'order_item_id': order_item_obj.pk,
        'cart_pk': order_item_obj.cart_id
    }
    return context
