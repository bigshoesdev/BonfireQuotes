# Generated by Django 2.2.5 on 2019-11-22 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0028_quotecollections_quote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='feature_qotd',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Featured QOTD'),
        ),
    ]
