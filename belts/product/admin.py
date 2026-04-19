from django.contrib import admin
from django.utils.html import format_html

from belts.product.models import Category, Product, ProductImage

admin.site.site_header = "Администрирование FABIS CRAFT"
admin.site.site_title = "FABIS CRAFT"
admin.site.index_title = "Панель управления"


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    verbose_name = "Изображение"
    verbose_name_plural = "Изображения товара"
    fields = ("image", "is_main", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {}
    readonly_fields = ()
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock_badge",
        "available",
        "created_at",
    )
    list_filter = ("available", "category", "created_at")
    search_fields = ("name", "description", "category__name")
    list_editable = ("price", "available")
    readonly_fields = ("slug", "created_at", "updated_at")
    inlines = [ProductImageInline]
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("category", "name", "description"),
            },
        ),
        (
            "Параметры товара",
            {
                "fields": ("price", "available", "stock"),
            },
        ),
        (
            "Системные поля",
            {
                "fields": ("slug", "created_at", "updated_at"),
            },
        ),
    )
    ordering = ("-created_at",)

    @admin.display(description="Остаток")
    def stock_badge(self, obj):
        if obj.stock == 0:
            color = "#d9534f"
            text = "Нет в наличии"
        elif obj.stock <= 3:
            color = "#f0ad4e"
            text = f"Мало: {obj.stock} шт."
        else:
            color = "#5cb85c"
            text = f"В наличии: {obj.stock} шт."

        return format_html(
            '<span style="'
            'display:inline-block;'
            'padding:4px 10px;'
            'border-radius:999px;'
            'font-weight:600;'
            'color:white;'
            'background:{};'
            '">{}</span>',
            color,
            text,
        )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_main", "created_at")
    list_filter = ("is_main", "created_at")
    search_fields = ("product__name",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)