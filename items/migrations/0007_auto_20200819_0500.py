# Generated by Django 3.1 on 2020-08-19 05:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20200817_0821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='quantity',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
