# Generated by Django 3.2.13 on 2022-05-09 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vinyl', '0003_alter_artist_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinyl',
            name='genres',
            field=models.ManyToManyField(related_name='genres', to='vinyl.Genre'),
        ),
    ]
