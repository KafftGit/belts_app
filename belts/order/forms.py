from django import forms

from belts.product.models import Product


class OrderCreateForm(forms.Form):
    items = forms.JSONField()
    address = forms.CharField()
    extra_notes = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_items(self):
        items = self.cleaned_data.get("items")
        if not isinstance(items, list) or not items:
            raise forms.ValidationError("Отсутствуют товары")

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

        order_items = []
        total_price = 0
        total_quantity = 0

        for product_id, quantity in aggregated.items():
            product = products_by_id[product_id]
            if product.stock_quantity < quantity:
                raise forms.ValidationError("Невозможно добавить столько товаров")
            item_total_price = int(product.price * quantity)
            order_items.append(
                {
                    "product": product,
                    "quantity": quantity,
                    "total_price": item_total_price,
                }
            )
            total_price += item_total_price
            total_quantity += quantity

        self.cleaned_data["order_items"] = order_items
        self.cleaned_data["total_price"] = total_price
        self.cleaned_data["total_quantity"] = total_quantity
        return items
