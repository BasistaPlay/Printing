# Generated by Django 4.2.7 on 2024-03-23 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_alter_imagelist_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagelist',
            name='image_png',
            field=models.ImageField(blank=True, upload_to='upload_images_orders/png/'),
        ),
    ]
