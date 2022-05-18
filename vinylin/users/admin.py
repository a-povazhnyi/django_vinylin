from django.contrib import admin
from django.urls import path

from .views import AddBalanceAdminView
from .models import User, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/profile_change_list.html'
    list_display = ('id', 'user')
    list_display_links = ('id', 'user')
    save_on_top = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('balance/',
                 self.add_balance_view,
                 name='add_balance')
        ]
        urls = custom_urls + urls
        return urls

    def add_balance_view(self, request):
        context = dict(self.admin_site.each_context(request))
        return AddBalanceAdminView.as_view()(request, admin_context=context)


admin.site.register(User)
