# Generated by Django 4.2.7 on 2024-08-14 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Virsraksts')),
                ('title_lv', models.CharField(max_length=100, null=True, verbose_name='Virsraksts')),
                ('title_en', models.CharField(max_length=100, null=True, verbose_name='Virsraksts')),
                ('description', models.TextField(verbose_name='Apraksts')),
                ('description_lv', models.TextField(null=True, verbose_name='Apraksts')),
                ('description_en', models.TextField(null=True, verbose_name='Apraksts')),
                ('additional_notes', models.TextField(verbose_name='Papildu piezīmes')),
                ('additional_notes_lv', models.TextField(null=True, verbose_name='Papildu piezīmes')),
                ('additional_notes_en', models.TextField(null=True, verbose_name='Papildu piezīmes')),
                ('image', models.ImageField(upload_to='page/', verbose_name='Bilde')),
            ],
            options={
                'verbose_name': 'Pielāgots dizains',
                'verbose_name_plural': 'Pielāgoti dizaini',
            },
        ),
        migrations.CreateModel(
            name='GiftCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('is_valid', models.BooleanField(default=True)),
                ('discount_type', models.CharField(choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')], max_length=20)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_order_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('unlimited_usage', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Dāvanu kods',
                'verbose_name_plural': 'Dāvanu kodi',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('PENDING', 'Gaida apstiprinājumu'), ('PROCESSING', 'Apstrāde'), ('SHIPPED', 'Nosūtīts'), ('DELIVERED', 'Piegādāts'), ('CANCELLED', 'Atcelts')], default='PENDING', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
                ('purchase', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase_products', to='home.purchase')),
            ],
        ),
    ]
