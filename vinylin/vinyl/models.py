from django.db import models

from store.models import Product


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


class Artist(models.Model):
    name = models.CharField(max_length=200)
    overview = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Vinyl(Product):
    vinyl_title = models.CharField(max_length=150)
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
    )
    genre = models.ManyToManyField(Genre)
    country = models.ForeignKey(
        to=Country,
        null=True,
        on_delete=models.SET_NULL,
    )
    format = models.CharField(max_length=50, blank=True, null=True)
    credits = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.title
