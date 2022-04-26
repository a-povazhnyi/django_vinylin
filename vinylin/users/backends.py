from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


UserModel = get_user_model()


class EmailSignInBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(
                Q(email__iexact=username)).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
            return user


class EmailConfirmMessage(EmailMessage):
    def __init__(self, code, *args, **kwargs):
        """to keyword argument should be specified during initialization"""
        super().__init__(*args, **kwargs)

        self.code = code
        self.from_email = 'jooomanfirst@yandex.ru'
        self.subject = 'Confirm your e-mail'
        self.body = f'Here is your e-mail verification code: \n{self.code}'
