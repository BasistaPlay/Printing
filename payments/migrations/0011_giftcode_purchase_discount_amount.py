# Generated by Django 4.2.7 on 2024-10-06 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_purchase_comments_purchase_company_address_and_more'),
    ]

    operations = [
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
        migrations.AddField(
            model_name='purchase',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]