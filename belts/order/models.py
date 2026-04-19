from django.conf import settings
from django.db import models

from belts.product.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("NEW", "Новый"),
        ("PROCESSING", "В обработке"),
        ("COMPLETED", "Завершён"),
        ("CANCELLED", "Отменён"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="Пользователь",
    )
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default="NEW")
    total_price = models.DecimalField("Сумма заказа", max_digits=10, decimal_places=2, default=0)

    recipient_name = models.CharField("Получатель", max_length=255)
    phone = models.CharField("Телефон", max_length=30)
    city = models.CharField("Город", max_length=120)
    street = models.CharField("Улица", max_length=255)
    house = models.CharField("Дом", max_length=30)
    apartment = models.CharField("Квартира", max_length=30, blank=True)
    entrance = models.CharField("Подъезд", max_length=30, blank=True)
    floor = models.CharField("Этаж", max_length=30, blank=True)
    intercom = models.CharField("Домофон", max_length=30, blank=True)
    postal_code = models.CharField("Индекс", max_length=20, blank=True)

    address = models.TextField("Полный адрес", blank=True)
    extra_notes = models.TextField("Комментарий", blank=True)

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk}"

    def build_full_address(self) -> str:
        parts = [
            self.city,
            f"ул. {self.street}" if self.street else "",
            f"д. {self.house}" if self.house else "",
            f"кв. {self.apartment}" if self.apartment else "",
            f"подъезд {self.entrance}" if self.entrance else "",
            f"этаж {self.floor}" if self.floor else "",
            f"домофон {self.intercom}" if self.intercom else "",
        ]
        return ", ".join([part for part in parts if part])


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        verbose_name="Товар",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)
    unit_price = models.DecimalField("Цена за единицу", max_digits=10, decimal_places=2)
    total_price = models.DecimalField("Сумма позиции", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    def __str__(self):
        return f"{self.product} x {self.quantity}"