# Generated by Django 4.0.8 on 2022-12-14 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_pricehistory_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pricehistory',
            options={'ordering': ['-id'], 'verbose_name': 'История цен', 'verbose_name_plural': 'Истории цен'},
        ),
    ]
