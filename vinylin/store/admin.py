from django.contrib import admin

from .forms import ProductAdminForm
from .models import Category, Tag, Discount, Image, Product, Storage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    save_on_top = True


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Discount)
admin.site.register(Image)
admin.site.register(Storage)
