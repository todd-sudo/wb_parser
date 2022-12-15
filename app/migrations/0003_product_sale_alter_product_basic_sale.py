# Generated by Django 4.0.8 on 2022-11-01 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_product_date_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sale',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='basic_sale',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Основная скидка(Для авторизованных)'),
        ),
    ]
