# Generated by Django 3.2.13 on 2022-05-20 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vinyl', '0008_alter_vinyl_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinyl',
            name='artist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vinyl.artist'),
        ),
        migrations.AlterField(
            model_name='vinyl',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vinyl.country'),
        ),
        migrations.AlterField(
            model_name='vinyl',
            name='genres',
            field=models.ManyToManyField(to='vinyl.Genre'),
        ),
    ]