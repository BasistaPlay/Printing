# Generated by Django 4.2.7 on 2024-07-27 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_order_product_amount_order_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product_amount',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product_size',
        ),
    ]