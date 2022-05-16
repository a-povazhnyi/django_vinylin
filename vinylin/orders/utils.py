def count_total_price(order_items):
    total_price = 0
    for item in order_items:
        if item.product.price_with_discount:
            item_price = item.product.price_with_discount * item.quantity
            total_price += item_price
        else:
            item_price = item.product.price * item.quantity
            total_price += float(item_price)

    return round(total_price, 2)