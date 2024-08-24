# Generated by Django 4.2.7 on 2024-08-24 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0004_product_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='can_be_rotate',
            field=models.BooleanField(default=False, help_text='Norādiet, vai produktu var apgriezt.', verbose_name='Var tikt grozīts'),
        ),
        migrations.AddField(
            model_name='product',
            name='can_have_ai_image',
            field=models.BooleanField(default=False, help_text='Norādiet, vai produktā var būt attēls ar AI palīdzību.', verbose_name='Var ietvert attēlu ar AI palīdzību'),
        ),
        migrations.AddField(
            model_name='product',
            name='can_have_image',
            field=models.BooleanField(default=False, help_text='Norādiet, vai produktā var būt attēls.', verbose_name='Var ietvert attēlu'),
        ),
        migrations.AddField(
            model_name='product',
            name='can_have_text',
            field=models.BooleanField(default=False, help_text='Norādiet, vai produktā var būt teksts.', verbose_name='Var ietvert tekstu'),
        ),
    ]