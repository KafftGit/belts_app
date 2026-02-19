from django import forms

from product.models import Product


def validate_user_items(items: list) -> dict:
    aggregated = {}

    for item in items:

        if not isinstance(item, dict):
            raise forms.ValidationError("Не валидный формат данных")

        product_id = item.get("product_id")
        quantity = item.get("quantity")

        if not isinstance(product_id, int) or product_id < 1 or not isinstance(quantity, int) or quantity < 1:
            raise forms.ValidationError(f"Ошибка валидации")
        aggregated[product_id] = quantity

    products = Product.objects.filter(id__in=aggregated.keys(), available=True)
    products_by_id = {product.id: product for product in products}

    product_items = []
    total_price = 0
    total_quantity = 0

    for product_id, quantity in aggregated.items():
        product = products_by_id[product_id]
        if product.stock_quantity < quantity:
            raise forms.ValidationError("Невозможно добавить столько товаров")
        item_total_price = int(product.price * quantity)
        product_items.append(
            {
                "product": product,
                "quantity": quantity,
                "total_price": item_total_price,
            }
        )
        total_price += item_total_price
        total_quantity += quantity

    return {
        'total_price': total_price,
        'total_quantity': total_quantity,
        'product_items': product_items,
    }
