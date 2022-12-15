from django.db import models


class Proxy(models.Model):
    """ Модель прокси
    """
    username = models.CharField("Username", max_length=200)
    password = models.CharField("Password", max_length=200)
    host = models.CharField("Host", max_length=200)
    port = models.CharField("Port", max_length=200)

    def __str__(self):
        return f"{self.username}:{self.password}@{self.host}:{self.port}"

    class Meta:
        verbose_name = verbose_name_plural = "Proxy"


class Product1C(models.Model):
    """ Товар 1С
    """
    sku = models.CharField("SKU", max_length=300, unique=True)
    price = models.FloatField("Цена", default=0.0)
    date_updated = models.DateField("Дата обновления")

    def __str__(self):
        return f"[{self.sku}] {self.price} {self.date_updated}"

    class Meta:
        verbose_name = "Товар 1C"
        verbose_name_plural = "Товары 1C"


class ProductWB(models.Model):
    """ Товар WB
    """
    product_1c = models.OneToOneField(
        Product1C,
        on_delete=models.CASCADE,
        verbose_name="Товар 1С",
        related_name="product_wb"
    )

    is_check = models.BooleanField("Check", default=True)
    sku = models.CharField("Код товара", max_length=200, unique=True)
    root_id = models.CharField("Root ID", max_length=200)
    name = models.CharField("Название", max_length=500)
    brand = models.CharField("Бренд", max_length=500, null=True, blank=True)
    percentage = models.FloatField("Кол-во процентов", default=0)
    sale = models.PositiveIntegerField(
        "Скидка", blank=True, null=True, default=0
    )
    basic_sale = models.PositiveIntegerField(
        "Основная скидка(Для авторизованных)", blank=True, null=True, default=0
    )
    basic_price = models.PositiveIntegerField(
        "Цена с основной скидкой", blank=True, null=True, default=0
    )
    client_sale = models.PositiveIntegerField(
        "Скидка клиента", blank=True, null=True, default=0
    )
    client_price = models.PositiveIntegerField(
        "Цена с клиентской скидкой", blank=True, null=True, default=0
    )
    price = models.PositiveIntegerField(
        "Итоговая цена (ССП)", blank=True, null=True, default=0
    )
    price_old = models.PositiveIntegerField(
        "Старая цена", blank=True, null=True, default=0
    )
    price_no_sale = models.PositiveIntegerField(
        "Цена без скидок", blank=True, null=True, default=0
    )
    avg_price = models.PositiveIntegerField(
        "Средняя цена", blank=True, null=True, default=0
    )
    rating = models.PositiveIntegerField(
        "Рейтинг", blank=True, null=True, default=0
    )
    feedbacks = models.PositiveIntegerField(
        "Кол-во отзывов", blank=True, null=True, default=0
    )
    count_in_stock = models.PositiveIntegerField(
        "Кол-во товаров на складе", blank=True, null=True, default=0
    )
    count_in_stock_old = models.PositiveIntegerField(
        "[Начало] Кол-во товаров на складе",
        blank=True,
        null=True,
        default=0
    )
    is_active = models.BooleanField("В наличие", default=True)
    country = models.CharField(
        "Страна производства", max_length=1000, null=True, blank=True
    )
    url = models.CharField("URL", max_length=1000, null=True, blank=True)
    date_updated = models.DateField("Дата обновления")
    description = models.TextField("Описание", null=True, blank=True)
    
    def __str__(self):
        return f"[{self.sku}] {self.name}"

    class Meta:
        verbose_name = "Товар WB"
        verbose_name_plural = "Товары WB"


class PriceHistory(models.Model):
    """ История цен
    """
    product_wb = models.ForeignKey(
        ProductWB,
        on_delete=models.CASCADE,
        verbose_name="Товар WB",
        related_name="prices"
    )
    price = models.PositiveIntegerField(
        "Цена", blank=True, null=True, default=0
    )
    create_at = models.DateField("Дата создания")

    def __str__(self):
        return f"{self.product_wb} - {self.price}"

    class Meta:
        verbose_name = "История цен"
        verbose_name_plural = "Истории цен"
        ordering = ["-id"]


class Feedback(models.Model):
    """ Модель отзывов
    """
    product = models.ForeignKey(
        ProductWB,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Отзывы",
        related_name="feedbacks_set"
    )
    color = models.CharField("Цвет", max_length=300, null=True, blank=True)
    size = models.CharField("Размер", max_length=300, null=True, blank=True)
    username = models.CharField(
        "Пользователь", max_length=500, null=True, blank=True
    )
    text = models.TextField(
        "Текст отзыва", null=True, blank=True
    )
    create_at = models.CharField(
        "Дата создания отзыва", max_length=200, null=True, blank=True
    )
    answer = models.TextField("Ответ", null=True, blank=True)

    def __str__(self):
        return f"{self.product} - {self.username}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        
        
class Specification(models.Model):
    """ Модель характеристик товара
    """
    product = models.ForeignKey(
        ProductWB,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Отзывы",
        related_name="specs_set"
    )
    name = models.CharField("Название", max_length=500, null=True, blank=True)
    value = models.TextField("Значение", null=True, blank=True)

    def __str__(self):
        return f"{self.product}"
    
    class Meta:
        verbose_name = "Характеристики"
        verbose_name_plural = "Характеристика"
    
