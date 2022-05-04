from django.contrib import admin

from .models import Country, Genre, Artist, Vinyl


admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Vinyl)
