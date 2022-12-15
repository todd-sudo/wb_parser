# Generated by Django 4.0.8 on 2022-12-14 12:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_product_date_updated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product1C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=300, unique=True, verbose_name='SKU')),
                ('price', models.FloatField(default=0.0, verbose_name='Цена')),
                ('date_updated', models.DateField(verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Товар 1C',
                'verbose_name_plural': 'Товары 1C',
            },
        ),
        migrations.CreateModel(
            name='ProductWB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku', models.CharField(max_length=200, unique=True, verbose_name='Код товара')),
                ('root_id', models.CharField(max_length=200, verbose_name='Root ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название')),
                ('brand', models.CharField(blank=True, max_length=500, null=True, verbose_name='Бренд')),
                ('percentage', models.FloatField(default=0, verbose_name='Кол-во процентов')),
                ('sale', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Скидка')),
                ('basic_sale', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Основная скидка(Для авторизованных)')),
                ('basic_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Цена с основной скидкой')),
                ('client_sale', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Скидка клиента')),
                ('client_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Цена с клиентской скидкой')),
                ('price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Итоговая цена (ССП)')),
                ('price_old', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Старая цена')),
                ('price_no_sale', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Цена без скидок')),
                ('avg_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Средняя цена')),
                ('rating', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Рейтинг')),
                ('feedbacks', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Кол-во отзывов')),
                ('count_in_stock', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Кол-во товаров на складе')),
                ('count_in_stock_old', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='[Начало] Кол-во товаров на складе')),
                ('is_active', models.BooleanField(default=True, verbose_name='В наличие')),
                ('country', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Страна производства')),
                ('url', models.CharField(blank=True, max_length=1000, null=True, verbose_name='URL')),
                ('date_updated', models.DateField(verbose_name='Дата обновления')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('product_1c', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_wb', to='app.product1c', verbose_name='Товар 1С')),
            ],
            options={
                'verbose_name': 'Товар WB',
                'verbose_name_plural': 'Товары WB',
            },
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Цена')),
                ('create_at', models.DateField(verbose_name='Дата создания')),
                ('product_wb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='app.productwb', verbose_name='Товар WB')),
            ],
            options={
                'verbose_name': 'Товар WB',
                'verbose_name_plural': 'Товары WB',
            },
        ),
        migrations.AlterField(
            model_name='feedback',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks_set', to='app.productwb', verbose_name='Отзывы'),
        ),
        migrations.AlterField(
            model_name='specification',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='specs_set', to='app.productwb', verbose_name='Отзывы'),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
