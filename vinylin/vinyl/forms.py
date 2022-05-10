from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Vinyl
from store.utils import generate_part_number


class VinylAdminForm(forms.ModelForm):
    overview = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Vinyl
        fields = '__all__'
        widgets = {
            'part_number': forms.TextInput({'value': generate_part_number()})
        }
