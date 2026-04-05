from django.conf import settings
from django.db import models


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk} for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "product.Product",
        on_delete=models.PROTECT,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
    max_digits=10,
    decimal_places=2
)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_item_per_product",
            )
        ]

    def __str__(self):
        return f"{self.product} x{self.quantity}"
