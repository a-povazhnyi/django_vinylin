from django.contrib import admin

from .forms import VinylAdminForm
from .models import Country, Genre, Artist, Vinyl
from store.admin import ImageInlineAdmin, StorageInlineAdmin, DiscountInlineAdmin


@admin.register(Vinyl)
class VinylAdmin(admin.ModelAdmin):
    form = VinylAdminForm
    readonly_fields = ('created_at',)
    list_display = ('id', 'title', 'price', 'part_number')
    list_display_links = ('id', 'title')
    inlines = [ImageInlineAdmin, StorageInlineAdmin, DiscountInlineAdmin]

    save_on_top = True

    def get_readonly_fields(self, request, obj=None):
        """Adds price_with_discount field if it exists"""
        readonly_fields = super().get_readonly_fields(request, obj)
        try:
            if not obj.price_with_discount:
                return readonly_fields
        except AttributeError:
            return readonly_fields
        return ['price_with_discount', *readonly_fields]

    def get_fields(self, request, obj=None):
        """Puts price_with_discount in position after price"""
        fields = super().get_fields(request, obj)
        try:
            if not obj.price_with_discount:
                return fields
        except AttributeError:
            return fields

        price_index = fields.index('price')
        fields.insert(price_index + 1, 'price_with_discount')
        return fields


admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Artist)
