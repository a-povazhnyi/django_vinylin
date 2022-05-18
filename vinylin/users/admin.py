from django.contrib import admin
from django.urls import path

from .views import AddBalanceAdminView
from .models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'is_email_verified')
    list_display_links = ('id', 'email', 'full_name')

    @staticmethod
    def full_name(obj):
        return f'{obj.first_name} {obj.last_name}'


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    change_list_template = 'admin/profile_change_list.html'
    change_form_template = 'admin/profile_change_form.html'
    list_display = ('id', 'user', 'age', 'country')
    list_display_links = ('id', 'user')
    save_on_top = True

    def change_view(self, request, object_id, form_url='', extra_context=None):
        context = {'object_id': object_id}
        return super().change_view(request, object_id, extra_context=context)

    def get_urls(self):
        urls = super().get_urls()
        additional_urls = [
            path('balance/', self.add_balance_view, name='add_balance'),
            path('<path:object_id>/change/balance/',
                 self.add_one_balance_view,
                 name='add_one_balance')
        ]
        return additional_urls + urls

    def add_balance_view(self, request):
        context = dict(self.admin_site.each_context(request))
        return AddBalanceAdminView.as_view()(request, admin_context=context)

    def add_one_balance_view(self, request, object_id):
        context = dict(self.admin_site.each_context(request))
        context['object_id'] = int(object_id)
        return AddBalanceAdminView.as_view()(request, admin_context=context)
