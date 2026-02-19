from django.db import transaction
from django.http import JsonResponse

from cart.forms import CartCreateForm, CartItemDeleteForm
from cart.models import Cart, CartItem


class CartViewManager:

    def create(self, request):
        data = request.POST

        form = CartCreateForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            CartItem.objects.create(
                cart=cart,
                **form.cleaned_data
            )

        return JsonResponse({"id": cart.id}, status=201)

    def update(self, request):
        data = request.POST

        form = CartCreateForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            item = CartItem.objects.get(product=form.cleaned_data["product"], cart=cart)

            item.quantity = form.cleaned_data["quantity"]
            item.unit_price = form.cleaned_data["unit_price"]
            item.save()

        return JsonResponse({"id": cart.id}, status=201)

    def delete(self, request):
        data = request.POST

        form = CartItemDeleteForm(data)

        if not form.is_valid():
            return JsonResponse({"errors": form.errors}, status=400)

        with transaction.atomic():
            cart, _ = Cart.objects.get_or_create(user=request.user)

            CartItem.objects.get(product=form.cleaned_data["product"], cart=cart).delete()

        return JsonResponse({"id": cart.id}, status=201)
