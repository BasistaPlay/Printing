# Generated by Django 4.2.7 on 2024-08-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_remove_product_available_colors_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_public',
            field=models.BooleanField(default=True, help_text='Norādiet, vai produkts ir publisks.', verbose_name='Publisks'),
        ),
    ]
