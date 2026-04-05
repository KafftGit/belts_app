from django.conf import settings
from django.db import models

class Status(models.TextChoices):
    APPROVED = "APPROVED", "Approved"
    DECLINED = "DECLINED", "Declined"
    CANCELED = "CANCELED", "Canceled"
    DONE = "DONE", "Done"
    NEW = "NEW", "New"
    PROCESSING = "PROCESSING", "Processing"

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Общая сумма заказа с учётом всех позиций"
    )
    address = models.TextField()
    extra_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.user.username}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Orders"
        verbose_name_plural = "Orders"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(
        help_text="Количество товара в заказе"
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Цена за единицу товара на момент заказа"
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Итоговая сумма для этой позиции (quantity × unit_price)"
    )

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    class Meta:
        verbose_name = "Order items"
        verbose_name_plural = "Order items"

