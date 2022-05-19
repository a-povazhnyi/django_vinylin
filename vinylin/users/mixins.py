from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)


class SignRequiredMixin(LoginRequiredMixin):
    login_url = '/users/sign-in/'
    redirect_field_name = ''


class AdminPermissionMixin(PermissionRequiredMixin):
    permission_required = (
        'users.add_user',
        'users.change_user',
        'users.delete_user',
        'users.view_user',
        'users.add_profile',
        'users.change_profile',
        'users.delete_profile',
        'users.view_profile'
    )
