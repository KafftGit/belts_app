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
        total_price = form.cleaned_data["total_price"]
        address = form.cleaned_data["address"]
        extra_notes = form.cleaned_data["extra_notes"]

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                address=address,
                extra_notes=extra_notes,
            )
            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        product=item["product"],
                        quantity=item["quantity"],
                        unit_price=item["product"].price,
                        total_price=item["total_price"],
                    )
                    for item in product_items
                ]
            )

        return JsonResponse({"id": order.id}, status=201)
