from django.db.models import Manager, DecimalField, F, Q, Case, When


class OrderItemManager(Manager):
    def get_queryset(self):
        queryset = (
            super().get_queryset()
            .select_related('product', 'product__discount')
            .prefetch_related('product__images')
            .prefetch_related('product__tags')
            .annotate(final_price=Case(
                When(
                    product__discount__amount=None,
                    then=F('product__price') * F('quantity')
                ),
                When(
                    product__discount__amount=Q(product__discount__amount__isnull=False),
                    then=(F('product__price') * (1 - (F('product__discount__amount') * self.get_decimal(0.01)))) * F('quantity'))
                ))
        )
        return queryset

    @staticmethod
    def get_decimal(value):
        return DecimalField(
            max_digits=6, decimal_places=2
        ).clean(str(value), None)
