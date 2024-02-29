# Generated by Django 4.2.7 on 2024-02-24 14:39

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_rename_max_usage_giftcode_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=25, samples=None)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='link',
        ),
        migrations.AddField(
            model_name='product',
            name='back_image_not_background',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Aizmugurējā bilde bez fona'),
        ),
        migrations.AddField(
            model_name='product',
            name='back_image_with_background',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Aizmugurējā bilde ar fonu'),
        ),
        migrations.AddField(
            model_name='product',
            name='front_image_not_background',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Priekšējā bilde bez fona'),
        ),
        migrations.AddField(
            model_name='product',
            name='front_image_with_background',
            field=models.ImageField(blank=True, upload_to='products/', verbose_name='Priekšējā bilde ar fonu'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='test', help_text='Ievadiet URL draudzīgu nosaukumu.', unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='available_colors',
            field=models.ManyToManyField(blank=True, related_name='products', to='home.color'),
        ),
    ]
