from django.db import transaction
from django.db.models import F, Sum, DecimalField
from django.http import JsonResponse

from belts.cart.forms import CartCreateForm, CartItemDeleteForm, CartCompleteForm
from belts.cart.models import Cart, CartItem
from belts.order.models import Order, OrderItem


class CartViewManager:

    def create(self, request):
        data = request.POST
        form = CartCreateForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            try:
                item = CartItem.objects.get(
                    product_id=form.cleaned_data["product"],
                    cart=cart,
                )
                item.quantity += form.cleaned_data["quantity"]
                item.save()
            except CartItem.DoesNotExist:
                from belts.product.models import Product
                product = Product.objects.get(id=form.cleaned_data["product"])

                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=form.cleaned_data["quantity"],
                    unit_price=product.price,
                )

        return JsonResponse({"id": cart.id}, status=201)

    def update(self, request, data=None):
        data = data or request.POST
        form = CartCreateForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            item = CartItem.objects.get(
                product_id=form.cleaned_data["product"],
                cart=cart,
            )
            item.quantity = form.cleaned_data["quantity"]
            item.save()

        return JsonResponse({"id": cart.id}, status=201)

    def delete(self, request, data=None):
        data = data or request.POST
        form = CartItemDeleteForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            CartItem.objects.get(
                product_id=form.cleaned_data["product"],
                cart=cart,
            ).delete()

        return JsonResponse({"id": cart.id}, status=201)

    def complete_order(self, request, data=None):
        data = data or request.POST
        form = CartCompleteForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        items = CartItem.objects.filter(cart__user=request.user).select_related("product")

        items_total_price = (
            items.aggregate(
                total=Sum(
                    F("unit_price") * F("quantity"),
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                )
            )["total"] or 0
        )

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=items_total_price,
                address=form.cleaned_data["address"],
                extra_notes=form.cleaned_data["extra_notes"],
            )

            OrderItem.objects.bulk_create([
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.unit_price * item.quantity,
                )
                for item in items
            ])

            items.delete()

        return JsonResponse({"id": order.id}, status=201)