# from django.db import transaction
# from django.db.models import F, Sum, DecimalField
# from django.http import JsonResponse

# from belts.cart.forms import CartCreateForm, CartItemDeleteForm, CartCompleteForm
# from belts.cart.models import Cart, CartItem
# from belts.order.models import Order, OrderItem


# class CartViewManager:

#     def create(self, request):
#         data = request.POST
#         form = CartCreateForm(data)

#         if not form.is_valid():
#             return JsonResponse({"errors": form.errors}, status=400)

#         with transaction.atomic():
#             cart, _ = Cart.objects.get_or_create(user=request.user)

#             try:
#                 item = CartItem.objects.get(
#                     product_id=form.cleaned_data["product"],
#                     cart=cart,
#                 )
#                 item.quantity += form.cleaned_data["quantity"]
#                 item.save()
#             except CartItem.DoesNotExist:
#                 from belts.product.models import Product
#                 product = Product.objects.get(id=form.cleaned_data["product"])

#                 CartItem.objects.create(
#                     cart=cart,
#                     product=product,
#                     quantity=form.cleaned_data["quantity"],
#                     unit_price=product.price,
#                 )

#         return JsonResponse({"id": cart.id}, status=201)

#     def update(self, request, data=None):
#         data = data or request.POST
#         form = CartCreateForm(data)

#         if not form.is_valid():
#             return JsonResponse({"errors": form.errors}, status=400)

#         with transaction.atomic():
#             cart, _ = Cart.objects.get_or_create(user=request.user)
#             item = CartItem.objects.get(
#                 product_id=form.cleaned_data["product"],
#                 cart=cart,
#             )
#             item.quantity = form.cleaned_data["quantity"]
#             item.save()

#         return JsonResponse({"id": cart.id}, status=201)

#     def delete(self, request, data=None):
#         data = data or request.POST
#         form = CartItemDeleteForm(data)

#         if not form.is_valid():
#             return JsonResponse({"errors": form.errors}, status=400)

#         with transaction.atomic():
#             cart, _ = Cart.objects.get_or_create(user=request.user)
#             CartItem.objects.get(
#                 product_id=form.cleaned_data["product"],
#                 cart=cart,
#             ).delete()

#         return JsonResponse({"id": cart.id}, status=201)

#     def complete_order(self, request, data=None):
#         data = data or request.POST
#         form = CartCompleteForm(data)

#         if not form.is_valid():
#             return JsonResponse({"errors": form.errors}, status=400)

#         items = CartItem.objects.filter(cart__user=request.user).select_related("product")

#         items_total_price = (
#             items.aggregate(
#                 total=Sum(
#                     F("unit_price") * F("quantity"),
#                     output_field=DecimalField(max_digits=10, decimal_places=2),
#                 )
#             )["total"] or 0
#         )

#         with transaction.atomic():
#             order = Order.objects.create(
#                 user=request.user,
#                 total_price=items_total_price,
#                 address=form.cleaned_data["address"],
#                 extra_notes=form.cleaned_data["extra_notes"],
#             )

#             OrderItem.objects.bulk_create([
#                 OrderItem(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                     unit_price=item.unit_price,
#                     total_price=item.unit_price * item.quantity,
#                 )
#                 for item in items
#             ])

#             items.delete()

#         return JsonResponse({"id": order.id}, status=201)
from django.db import transaction
from django.http import JsonResponse

from belts.cart.forms import (
    CartCompleteForm,
    CartCreateForm,
    CartItemDeleteForm,
    CartItemUpdateForm,
)
from belts.cart.models import Cart, CartItem
from belts.order.models import Order, OrderItem
from belts.product.models import Product


class CartViewManager:
    @staticmethod
    def _cart_total(cart):
        return sum(item.unit_price * item.quantity for item in cart.items.select_related("product").all())

    def create(self, request):
        data = request.POST
        form = CartCreateForm(data)

        if not form.is_valid():
            return JsonResponse(
                {
                    "detail": "Ошибка валидации формы добавления товара",
                    "errors": form.errors,
                },
                status=400,
            )

        product_id = form.cleaned_data["product"]
        quantity_to_add = form.cleaned_data["quantity"]

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return JsonResponse({"detail": "Товар не найден"}, status=404)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            try:
                item = CartItem.objects.get(
                    product_id=product_id,
                    cart=cart,
                )
                new_quantity = item.quantity + quantity_to_add

                if new_quantity > product.stock:
                    return JsonResponse(
                        {"detail": f"В наличии только {product.stock} шт. товара"},
                        status=400,
                    )

                item.quantity = new_quantity
                item.unit_price = product.price
                item.save(update_fields=["quantity", "unit_price"])
            except CartItem.DoesNotExist:
                if quantity_to_add > product.stock:
                    return JsonResponse(
                        {"detail": f"В наличии только {product.stock} шт. товара"},
                        status=400,
                    )

                item = CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=quantity_to_add,
                    unit_price=product.price,
                )

        return JsonResponse(
            {
                "id": cart.id,
                "item_quantity": item.quantity,
                "item_total_price": item.unit_price * item.quantity,
                "cart_total_price": self._cart_total(cart),
            },
            status=201,
        )

    def update_quantity(self, request, data=None):
        data = data or request.POST
        form = CartItemUpdateForm(data)

        if not form.is_valid():
            return JsonResponse(
                {
                    "detail": "Ошибка валидации формы изменения количества",
                    "errors": form.errors,
                },
                status=400,
            )

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            try:
                item = CartItem.objects.select_related("product").get(
                    product_id=form.cleaned_data["product"],
                    cart=cart,
                )
            except CartItem.DoesNotExist:
                return JsonResponse({"detail": "Товар не найден в корзине"}, status=404)

            if form.cleaned_data["quantity"] > item.product.stock:
                return JsonResponse(
                    {"detail": f"В наличии только {item.product.stock} шт. товара"},
                    status=400,
                )

            item.quantity = form.cleaned_data["quantity"]
            item.save(update_fields=["quantity"])

        return JsonResponse(
            {
                "id": cart.id,
                "product_id": item.product_id,
                "item_quantity": item.quantity,
                "unit_price": item.unit_price,
                "item_total_price": item.unit_price * item.quantity,
                "cart_total_price": self._cart_total(cart),
            },
            status=200,
        )

    def change_quantity(self, request, data=None):
        data = data or request.POST

        product_id = data.get("product")
        action = data.get("action")

        if not product_id or action not in {"increase", "decrease"}:
            return JsonResponse(
                {"detail": "Некорректные данные"},
                status=400,
            )

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            try:
                item = CartItem.objects.select_related("product").get(
                    product_id=product_id,
                    cart=cart,
                )
            except CartItem.DoesNotExist:
                return JsonResponse({"detail": "Товар не найден в корзине"}, status=404)

            if action == "increase":
                if item.quantity + 1 > item.product.stock:
                    return JsonResponse(
                        {"detail": f"В наличии только {item.product.stock} шт. товара"},
                        status=400,
                    )

                item.quantity += 1
                item.save(update_fields=["quantity"])
                removed = False
            else:
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save(update_fields=["quantity"])
                    removed = False
                else:
                    item.delete()
                    removed = True

        cart.refresh_from_db()

        return JsonResponse(
            {
                "product_id": int(product_id),
                "removed": removed,
                "item_quantity": None if removed else item.quantity,
                "unit_price": None if removed else item.unit_price,
                "item_total_price": None if removed else item.unit_price * item.quantity,
                "cart_total_price": self._cart_total(cart),
            },
            status=200,
        )

    def delete(self, request, data=None):
        data = data or request.POST
        form = CartItemDeleteForm(data)

        if not form.is_valid():
            return JsonResponse(
                {
                    "detail": "Ошибка валидации формы удаления товара",
                    "errors": form.errors,
                },
                status=400,
            )

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            try:
                CartItem.objects.get(
                    product_id=form.cleaned_data["product"],
                    cart=cart,
                ).delete()
            except CartItem.DoesNotExist:
                return JsonResponse({"detail": "Товар не найден в корзине"}, status=404)

        return JsonResponse(
            {
                "id": cart.id,
                "product_id": form.cleaned_data["product"],
                "removed": True,
                "cart_total_price": self._cart_total(cart),
            },
            status=200,
        )

    def complete_order(self, request, data=None):
        data = data or request.POST
        form = CartCompleteForm(data)

        if not form.is_valid():
            return JsonResponse(
                {
                    "detail": "Ошибка валидации формы оформления заказа",
                    "errors": form.errors,
                },
                status=400,
            )

        items = CartItem.objects.filter(cart__user=request.user).select_related("product")

        if not items.exists():
            return JsonResponse({"detail": "Корзина пуста"}, status=400)

        with transaction.atomic():
            for item in items:
                if item.quantity > item.product.stock:
                    return JsonResponse(
                        {"detail": f"Недостаточно товара «{item.product.name}». В наличии: {item.product.stock}"},
                        status=400,
                    )

            order_total_price = sum(item.unit_price * item.quantity for item in items)

            full_address_parts = [
                form.cleaned_data["city"],
                f"ул. {form.cleaned_data['street']}",
                f"д. {form.cleaned_data['house']}",
                f"кв. {form.cleaned_data['apartment']}" if form.cleaned_data["apartment"] else "",
                f"подъезд {form.cleaned_data['entrance']}" if form.cleaned_data["entrance"] else "",
                f"этаж {form.cleaned_data['floor']}" if form.cleaned_data["floor"] else "",
                f"домофон {form.cleaned_data['intercom']}" if form.cleaned_data["intercom"] else "",
            ]
            full_address = ", ".join([part for part in full_address_parts if part])

            order = Order.objects.create(
                user=request.user,
                total_price=order_total_price,
                recipient_name=form.cleaned_data["recipient_name"],
                phone=form.cleaned_data["phone"],
                city=form.cleaned_data["city"],
                street=form.cleaned_data["street"],
                house=form.cleaned_data["house"],
                apartment=form.cleaned_data["apartment"],
                entrance=form.cleaned_data["entrance"],
                floor=form.cleaned_data["floor"],
                intercom=form.cleaned_data["intercom"],
                postal_code=form.cleaned_data["postal_code"],
                address=full_address,
                extra_notes=form.cleaned_data["extra_notes"],
            )

            OrderItem.objects.bulk_create(
                [
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        unit_price=item.unit_price,
                        total_price=item.unit_price * item.quantity,
                    )
                    for item in items
                ]
            )

            for item in items:
                product = item.product
                product.stock -= item.quantity
                product.save(update_fields=["stock"])

            items.delete()

        return JsonResponse({"id": order.id}, status=201)