# Generated by Django 4.0.8 on 2022-12-14 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_product1c_productwb_pricehistory_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricehistory',
            options={'ordering': ['-create_at'], 'verbose_name': 'Товар WB', 'verbose_name_plural': 'Товары WB'},
        ),
    ]
