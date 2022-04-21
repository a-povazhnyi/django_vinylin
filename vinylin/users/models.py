from django.db import models
from django.contrib.auth.models import User

from vinyl.models import Country


class Profile(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    is_email_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(blank=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        related_name='country')

    def __str__(self):
        return f'{self.user_id} ({self.pk})'
