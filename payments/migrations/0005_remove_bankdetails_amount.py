# Generated by Django 4.2.7 on 2024-09-16 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_remove_bankdetails_is_paid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankdetails',
            name='amount',
        ),
    ]
