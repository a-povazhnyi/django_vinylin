from django.contrib.auth.mixins import UserPassesTestMixin


class UserOrdersPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.cart.pk == self.kwargs['cart_pk']
