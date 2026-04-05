from django import forms
import logging
from belts.utils.validators import validate_user_items

logger = logging.getLogger(__name__)

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

        validated_items = validate_user_items(items=items, user=self.user)

        total_order_price = 0
        processed_items = []

        for item_data in validated_items:
            product = item_data["product"]
            quantity = item_data["quantity"]

            # Проверка на корректность quantity
            if not isinstance(quantity, int) or quantity <= 0:
                raise forms.ValidationError("Количество товара должно быть положительным целым числом.")

            unit_price = product.price

            # Проверка на корректность unit_price
            if unit_price is None or unit_price < 0:
                raise forms.ValidationError(f"Цена товара '{product.name}' некорректна.")

            # Рассчитываем общую стоимость для текущего товара
            item_total_price = quantity * unit_price

            # Проверка на правильность расчета
            if item_total_price <= 0:
                raise forms.ValidationError(f"Общая стоимость товара '{product.name}' некорректна.")

            processed_item = {
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": item_total_price,
            }
            processed_items.append(processed_item)
            total_order_price += item_total_price

            # Логирование для отладки
            logger.debug(f"Product: {product.name}, Quantity: {quantity}, Unit Price: {unit_price}, Total Price: {item_total_price}")

        # Сохраняем обработанные данные в cleaned_data
        self.cleaned_data["product_items"] = processed_items
        self.cleaned_data["total_price"] = total_order_price

        # Логирование общей суммы заказа
        logger.debug(f"Total Order Price: {total_order_price}")

        return items
