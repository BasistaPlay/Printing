# Generated by Django 4.2.7 on 2024-08-14 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0001_initial'),
        ('product_details', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Designs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('publish_product', models.BooleanField(default=False)),
                ('allow_publish', models.BooleanField(default=False)),
                ('front_image', models.ImageField(blank=True, upload_to='designs/')),
                ('back_image', models.ImageField(blank=True, upload_to='designs/')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('description', models.TextField(blank=True)),
                ('average_rating', models.FloatField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
                ('product_color', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product_details.color')),
            ],
            options={
                'verbose_name': 'Dizaini',
                'verbose_name_plural': 'Dizaini',
            },
        ),
        migrations.CreateModel(
            name='TextList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('font', models.CharField(blank=True, max_length=50)),
                ('text_size', models.CharField(blank=True, max_length=25)),
                ('text_color', models.CharField(blank=True, max_length=20)),
                ('designs_text', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='design.designs')),
            ],
        ),
        migrations.CreateModel(
            name='ImageList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField(blank=True)),
                ('designs_images', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='design.designs')),
            ],
        ),
    ]