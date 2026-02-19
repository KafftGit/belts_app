from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, IntegerField, Sum
from django.http import QueryDict
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView

from belts.cart.manager import CartViewManager
from belts.cart.models import Cart, CartItem


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart

    def get_object(self, queryset=None):
        return Cart.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.all()
        total_price = items.aggregate(
            total=Sum(F("unit_price") * F("quantity"), output_field=IntegerField())
        )["total"] or 0
        context["cart_total_price"] = total_price
        return context


class CartCreateView(LoginRequiredMixin, View):
    def post(self, request):
        response = CartViewManager().create(request)
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return response

    def put(self, request):
        data = QueryDict(request.body)
        return CartViewManager().update(request, data=data)

    def delete(self, request):
        return CartItem.objects.filter(cart_id=request.session["cart_id"]).delete()


class CartItemView(LoginRequiredMixin, View):
    def delete(self, request):
        data = QueryDict(request.body)
        response = CartViewManager().delete(request, data=data)
        next_url = data.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return response


class CartCompleteView(LoginRequiredMixin, View):
    def post(self, request):
        response = CartViewManager().complete_order(request)
        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return response
