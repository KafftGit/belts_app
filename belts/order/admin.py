from django.contrib import admin
from django.utils.html import format_html

from belts.order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    verbose_name = "Позиция"
    verbose_name_plural = "Позиции заказа"
    fields = ("product", "quantity", "unit_price", "total_price")
    readonly_fields = ("total_price",)
    autocomplete_fields = ("product",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status_badge",
        "total_price",
        "city",
        "recipient_name",
        "created_at",
    )
    list_filter = ("status", "created_at", "city")
    search_fields = ("user__username", "recipient_name", "phone", "city", "street")
    readonly_fields = ("created_at", "address")
    inlines = [OrderItemInline]
    ordering = ("-created_at",)

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("user", "status", "total_price", "created_at"),
            },
        ),
        (
            "Данные получателя",
            {
                "fields": ("recipient_name", "phone"),
            },
        ),
        (
            "Адрес доставки",
            {
                "fields": (
                    "city",
                    "street",
                    "house",
                    "apartment",
                    "entrance",
                    "floor",
                    "intercom",
                    "postal_code",
                    "address",
                ),
            },
        ),
        (
            "Дополнительно",
            {
                "fields": ("extra_notes",),
            },
        ),
    )

    @admin.display(description="Статус")
    def status_badge(self, obj):
        colors = {
            "NEW": "#5bc0de",
            "PROCESSING": "#f0ad4e",
            "COMPLETED": "#5cb85c",
            "CANCELLED": "#d9534f",
        }
        labels = dict(Order.STATUS_CHOICES)

        return format_html(
            '<span style="display:inline-block;padding:4px 10px;border-radius:999px;'
            'font-weight:600;color:white;background:{};">{}</span>',
            colors.get(obj.status, "#777"),
            labels.get(obj.status, obj.status),
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "unit_price", "total_price")
    search_fields = ("order__id", "product__name")
    autocomplete_fields = ("order", "product")