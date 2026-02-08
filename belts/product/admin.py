from django.contrib import admin

from belts.product.models import Product, ProductImage


admin.site.register(Product)
admin.site.register(ProductImage)
