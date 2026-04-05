from django.db import transaction
from django.http import JsonResponse

from belts.cart.models import CartItem
from belts.order.forms import OrderCreateForm
from belts.order.models import Order, OrderItem

class OrderViewManager:
    @staticmethod
    def create(request):
        data = request.POST
        form = OrderCreateForm(data)
        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        product_items = form.cleaned_data["product_items"]
        order_total_price = form.cleaned_data["total_price"]
        address = form.cleaned_data["address"]
        extra_notes = form.cleaned_data["extra_notes"]

        with transaction.atomic():
            # Создаём заказ с корректной общей суммой
            order = Order.objects.create(
                user=request.user,
                total_price=order_total_price,
                address=address,
                extra_notes=extra_notes,
            )

            # Создаём позиции заказа
            order_items_to_create = []
            for item in product_items:
                item_total_price = item["quantity"] * item["unit_price"]  # Рассчитываем общую стоимость для каждого товара
                order_items_to_create.append(OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    unit_price=item["unit_price"],
                    total_price=item_total_price,  # Используем рассчитанную общую стоимость
                ))

            OrderItem.objects.bulk_create(order_items_to_create)

        return JsonResponse({"id": order.id}, status=201)

