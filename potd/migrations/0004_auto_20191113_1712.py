# Generated by Django 2.2.5 on 2019-11-14 00:12

from django.db import migrations
import slugger.fields


class Migration(migrations.Migration):

    dependencies = [
        ('potd', '0003_auto_20191113_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photooftheday',
            name='slug',
            field=slugger.fields.AutoSlugField(populate_from='title'),
        ),
    ]
