from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView

from belts.cart.manager import CartViewManager
from belts.cart.models import CartItem


class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_items = list(
            CartItem.objects.filter(cart__user=self.request.user).select_related("product")
        )

        cart_total_price = 0
        cart_items_count = 0

        for item in cart_items:
            item.item_total_price = item.unit_price * item.quantity
            cart_total_price += item.item_total_price
            cart_items_count += item.quantity

        context["cart_items"] = cart_items
        context["cart_total_price"] = cart_total_price
        context["cart_items_count"] = cart_items_count
        return context


class CartCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CartViewManager().create(request)


class CartItemUpdateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CartViewManager().update_quantity(request)


class CartItemChangeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CartViewManager().change_quantity(request)


class CartItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CartViewManager().delete(request)


class CartCompleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        return CartViewManager().complete_order(request)