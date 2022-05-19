from django.core.exceptions import ObjectDoesNotExist


def count_total_price(order_items):
    total_price = 0
    for item in order_items:
        try:
            price_with_discount = item.product.discount.price_with_discount
            if price_with_discount:
                item_price = price_with_discount * item.quantity
            else:
                item_price = item.product.price * item.quantity
        except ObjectDoesNotExist:
            item_price = item.product.price * item.quantity
        total_price += float(item_price)

    return round(total_price, 2)
