# Generated by Django 4.2.7 on 2024-02-24 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_color_remove_product_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text='Ievadiet URL draudzīgu nosaukumu.', verbose_name='Slug'),
        ),
    ]