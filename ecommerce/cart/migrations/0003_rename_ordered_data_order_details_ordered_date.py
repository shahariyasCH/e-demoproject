# Generated by Django 5.1.5 on 2025-02-13 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_payment_order_details'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_details',
            old_name='ordered_data',
            new_name='ordered_date',
        ),
    ]
