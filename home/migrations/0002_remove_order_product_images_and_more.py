# Generated by Django 4.2.7 on 2024-03-19 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagelist',
            name='order_images',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='home.order'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='textlist',
            name='order_text',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='home.order'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagelist',
            name='image',
            field=models.ImageField(blank=True, upload_to='upload_images/'),
        ),
        migrations.AlterField(
            model_name='textlist',
            name='font',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='textlist',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='textlist',
            name='text_color',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='textlist',
            name='text_size',
            field=models.IntegerField(blank=True),
        ),
    ]
