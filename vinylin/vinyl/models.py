from django.db import models
from django.urls import reverse

from .managers import VinylManager
from store.models import Product, Storage


class Country(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['pk']


class Genre(models.Model):
    title = models.CharField(max_length=150)
    overview = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['pk']


class Artist(models.Model):
    name = models.CharField(max_length=200)
    overview = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Vinyl(Product):
    vinyl_title = models.CharField(max_length=150)
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
        null=True,
        related_name='artist',
    )
    genres = models.ManyToManyField(Genre, related_name='genres')
    country = models.ForeignKey(
        to=Country,
        null=True,
        on_delete=models.SET_NULL,
        related_name='country',
    )
    format = models.CharField(max_length=50, blank=True, null=True)
    credits = models.CharField(max_length=250, blank=True, null=True)

    objects = VinylManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vinyl_single', kwargs={'pk': self.pk})
