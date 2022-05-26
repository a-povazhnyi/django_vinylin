from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import OrderItem
from store.models import Storage


class OrderItemQuantityForm(forms.ModelForm):
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        product = self.instance.product

        if Storage.objects.get(product=product).quantity < quantity:
            raise ValidationError(
                _('There is not enough product in stock...')
            )
        return quantity

    class Meta:
        model = OrderItem
        fields = ('quantity',)
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'quantity-form'
            })
        }