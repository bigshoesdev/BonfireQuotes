# Generated by Django 2.2.6 on 2019-11-08 00:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0012_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='like',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
