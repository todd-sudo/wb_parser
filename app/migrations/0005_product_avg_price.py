# Generated by Django 4.0.8 on 2022-11-01 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_product_average_price_product_price_no_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='avg_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Средняя цена'),
        ),
    ]
