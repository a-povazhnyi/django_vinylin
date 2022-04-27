from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from vinyl.models import Country


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username} ({self.pk})'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.SmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(170)],
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='country'
    )
    balance = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.user} ({self.pk})'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
