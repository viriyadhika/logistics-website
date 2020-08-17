# Generated by Django 3.1 on 2020-08-17 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_borrow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='borrower',
        ),
        migrations.AlterField(
            model_name='borrow',
            name='item_borrowed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='item_borrow_record', to='items.item'),
        ),
    ]
