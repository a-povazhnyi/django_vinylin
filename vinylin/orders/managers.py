from django.db import models


class OrderItemManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related('cart')
            .select_related('order')
            .prefetch_related('product__images')
            .prefetch_related('product__tags')
            .select_related('product__discount')
        )
