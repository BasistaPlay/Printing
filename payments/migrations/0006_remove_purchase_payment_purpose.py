# Generated by Django 4.2.7 on 2024-09-16 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_remove_bankdetails_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='payment_purpose',
        ),
    ]
