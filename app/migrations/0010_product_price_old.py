# Generated by Django 4.0.8 on 2022-11-29 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_product_external_id_product_percentage_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price_old',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Старая цена'),
        ),
    ]