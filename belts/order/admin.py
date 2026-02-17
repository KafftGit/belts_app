from django.contrib import admin

from belts.order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(OrderItem)
