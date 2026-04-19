from rest_framework import serializers
from belts.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "available",
            "stock",
        ]