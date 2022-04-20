from django.db import models

from .data import countries


class Country(models.Model):
    name = models.CharField(max_length=200, choices=countries.COUNTRY_CHOICES)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
