from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from belts.cart.models import Cart, CartItem
from cart.manager import CartViewManager
from mixins import IsUserOwnerOfModelMixin


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartItemListView(LoginRequiredMixin, ListView):
    model = CartItem
    paginate_by = 16

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related("cart", "product")


class CartCreateView(IsUserOwnerOfModelMixin, View):
    def post(self, request):
        return CartViewManager().create(request)

    def put(self, request):
        return CartViewManager().update(request)

    def delete(self, request):
        return CartViewManager().delete(request)
