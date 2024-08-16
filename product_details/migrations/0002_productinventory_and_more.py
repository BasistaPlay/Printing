# Generated by Django 4.2.7 on 2024-08-16 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_initial'),
        ('product_details', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='Product.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_details.size')),
            ],
            options={
                'verbose_name': 'Noliktavas krājums',
                'verbose_name_plural': 'Noliktavas krājumi',
            },
        ),
        migrations.AddConstraint(
            model_name='productinventory',
            constraint=models.UniqueConstraint(condition=models.Q(('size__isnull', False)), fields=('product', 'color', 'size'), name='unique_inventory_item'),
        ),
        migrations.AddConstraint(
            model_name='productinventory',
            constraint=models.UniqueConstraint(condition=models.Q(('size__isnull', True)), fields=('product', 'color'), name='unique_inventory_item_without_size'),
        ),
    ]