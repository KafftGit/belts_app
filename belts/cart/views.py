# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models import F, Sum, DecimalField
# from django.http import QueryDict
# from django.shortcuts import redirect
# from django.views import View
# from django.views.generic import DetailView


# from belts.cart.manager import CartViewManager
# from belts.cart.models import Cart, CartItem


# class CartDetailView(LoginRequiredMixin, DetailView):
#     model = Cart

#     def get_object(self, queryset=None):
#         return Cart.objects.get_or_create(user=self.request.user)[0]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         items = self.object.items.all()
#         total_price = items.aggregate(
#             total=Sum(
#                 F("unit_price") * F("quantity"),
#                 output_field=DecimalField(max_digits=10, decimal_places=2)
#             )
#         )["total"] or 0
#         context["cart_total_price"] = total_price
#         return context


# class CartCreateView(LoginRequiredMixin, View):
#     def post(self, request):
#         response = CartViewManager().create(request)
#         next_url = request.POST.get("next")
#         if next_url:
#             return redirect(next_url)
#         return response

#     def put(self, request):
#         data = QueryDict(request.body)
#         return CartViewManager().update(request, data=data)

#     def delete(self, request):
#         return CartItem.objects.filter(cart_id=request.session["cart_id"]).delete()


# class CartItemView(LoginRequiredMixin, View):
#     def delete(self, request):
#         data = QueryDict(request.body)
#         response = CartViewManager().delete(request, data=data)
#         next_url = data.get("next") or request.GET.get("next")
#         if next_url:
#             return redirect(next_url)
#         return response


# class CartCompleteView(LoginRequiredMixin, View):
#     def post(self, request):
#         response = CartViewManager().complete_order(request)
#         next_url = request.POST.get("next")
#         if next_url:
#             return redirect(next_url)
#         return response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, IntegerField, Sum
from django.http import QueryDict
from django.shortcuts import redirect
from django.views import View
from django.views.generic import DetailView

from belts.cart.manager import CartViewManager
from belts.cart.models import Cart


class CartDetailView(LoginRequiredMixin, DetailView):
    model = Cart
    template_name = "cart/cart_detail.html"

    def get_object(self, queryset=None):
        return Cart.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.object.items.select_related("product").all()
        total_price = items.aggregate(
            total=Sum(F("unit_price") * F("quantity"), output_field=IntegerField())
        )["total"] or 0
        context["cart_items"] = items
        context["cart_total_price"] = total_price
        return context


class CartCreateView(LoginRequiredMixin, View):
    def post(self, request):
        response = CartViewManager().create(request)
        next_url = request.POST.get("next")
        if next_url and request.headers.get("x-requested-with") != "XMLHttpRequest":
            return redirect(next_url)
        return response


class CartItemUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        response = CartViewManager().update_quantity(request)
        next_url = request.POST.get("next")
        if next_url and request.headers.get("x-requested-with") != "XMLHttpRequest":
            return redirect(next_url)
        return response


class CartItemChangeView(LoginRequiredMixin, View):
    def post(self, request):
        return CartViewManager().change_quantity(request)


class CartItemView(LoginRequiredMixin, View):
    def post(self, request):
        response = CartViewManager().delete(request)
        next_url = request.POST.get("next")
        if next_url and request.headers.get("x-requested-with") != "XMLHttpRequest":
            return redirect(next_url)
        return response

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
        if next_url and request.headers.get("x-requested-with") != "XMLHttpRequest":
            return redirect(next_url)
        return response