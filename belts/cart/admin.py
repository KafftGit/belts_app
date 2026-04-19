from django.contrib import admin
from django.utils.html import format_html

from belts.cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    verbose_name = "Товар"
    verbose_name_plural = "Товары в корзине"
    fields = ("product", "quantity", "unit_price")
    autocomplete_fields = ("product",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "items_count", "updated_at")
    search_fields = ("user__username",)
    readonly_fields = ("created_at", "updated_at")
    inlines = [CartItemInline]
    ordering = ("-updated_at",)

    @admin.display(description="Количество товаров")
    def items_count(self, obj):
        count = obj.items.count()
        color = "#5cb85c" if count > 0 else "#d9534f"
        text = f"{count} шт."
        return format_html(
            '<span style="display:inline-block;padding:4px 10px;border-radius:999px;'
            'font-weight:600;color:white;background:{};">{}</span>',
            color,
            text,
        )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity", "unit_price")
    list_filter = ("cart__user",)
    search_fields = ("product__name", "cart__user__username")
    autocomplete_fields = ("cart", "product")