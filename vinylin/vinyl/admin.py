from django.contrib import admin

from .forms import VinylAdminForm
from .models import Country, Genre, Artist, Vinyl


@admin.register(Vinyl)
class VinylAdmin(admin.ModelAdmin):
    form = VinylAdminForm
    save_on_top = True


admin.site.register(Country)
admin.site.register(Genre)
admin.site.register(Artist)
