# Generated by Django 4.2.7 on 2024-03-23 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_textlist_text_alter_textlist_text_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagelist',
            name='image',
            field=models.ImageField(blank=True, upload_to='upload_images_orders/'),
        ),
    ]