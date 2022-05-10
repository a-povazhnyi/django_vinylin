from django.db import models

from store.models import Product
from users.models import User


class Cart(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.pk}) {self.user} Cart'


class Order(models.Model):
    STATUS_CHOICES = [
        ('NPA', 'not_paid'),
        ('PA', 'is_paid'),
        ('ODE', 'on_delivery'),
        ('DE', 'is_delivered'),
        ('CA', 'canceled'),
    ]
    user = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    total_price = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'({self.pk}) {self.user} Order'


class OrderItems(models.Model):
    cart = models.ForeignKey(to=Cart, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(to=Order, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(
        to=Product,
        null=True,
        on_delete=models.SET_NULL,
    )
    quantity = models.SmallIntegerField(default=1)
