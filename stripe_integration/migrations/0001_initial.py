# Generated by Django 4.2.7 on 2024-05-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StripeKeys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_key', models.CharField(max_length=100)),
                ('secret_key', models.CharField(max_length=100)),
                ('endpoint_secret', models.CharField(max_length=100)),
            ],
        ),
    ]
