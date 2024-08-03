# Generated by Django 4.2.7 on 2024-08-03 18:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0001_initial'),
        ('home', '0004_remove_order_product_amount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='available_colors',
        ),
        migrations.RemoveField(
            model_name='product',
            name='available_sizes',
        ),
        migrations.RemoveField(
            model_name='product',
            name='categories',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='order',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Pasūtījums', 'verbose_name_plural': 'Pasūtījumi'},
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.color'),
        ),
        migrations.AlterField(
            model_name='purchaseproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product'),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Color',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Rating',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
