# Generated by Django 4.2.7 on 2024-08-10 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='designs',
            options={'verbose_name': 'Dizaini', 'verbose_name_plural': 'Dizaini'},
        ),
        migrations.RemoveField(
            model_name='designs',
            name='product_color',
        ),
    ]
