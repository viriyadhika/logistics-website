# Generated by Django 3.1 on 2020-08-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to='<built-in function id>'),
        ),
    ]
