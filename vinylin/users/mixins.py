from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy


class SignRequiredMixin(LoginRequiredMixin):
    login_url = '/users/sign-in/'
    redirect_field_name = ''


class AnonymousOnlyMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_anonymous

    def dispatch(self, request, *args, **kwargs):
        user_test_result = self.get_test_func()()
        if not user_test_result:
            return redirect(reverse_lazy('sign_exceptions'))
        return super().dispatch(request, *args, **kwargs)


class ProfileOwnViewMixin:
    @staticmethod
    def _is_user_owner(request, **kwargs):
        return request.user.pk == kwargs.get('pk')

    def get(self, request, *args, **kwargs):
        if not self._is_user_owner(request, **kwargs):
            context = {
                'alert_message': ('You have not enough permissions '
                                  'to see this page'),
                'redirect_url': reverse_lazy('index'),
            }
            return render(request, 'alert.html', context)
        return super().get(request, *args, **kwargs)


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
