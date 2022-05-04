from django.contrib import admin

from .models import Category, Tag, Sale, Image, Product, Storage


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Sale)
admin.site.register(Image)
admin.site.register(Product)
admin.site.register(Storage)
