from django import forms

from .models import Vinyl
from store.utils import generate_part_number


class VinylAdminForm(forms.ModelForm):
    class Meta:
        model = Vinyl
        fields = '__all__'
        widgets = {
            'part_number': forms.TextInput({'value': generate_part_number()})
        }
