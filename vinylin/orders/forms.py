from django import forms

from .models import OrderItem


class OrderItemQuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ('quantity',)
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'quantity-form'
            })
        }
