from django.contrib.auth.mixins import LoginRequiredMixin


class SignRequiredMixin(LoginRequiredMixin):
    login_url = '/users/sign-in/'
    redirect_field_name = ''
