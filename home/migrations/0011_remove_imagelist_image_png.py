# Generated by Django 4.2.7 on 2024-03-23 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_imagelist_image_png'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagelist',
            name='image_png',
        ),
    ]
