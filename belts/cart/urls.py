from django.urls import path

from belts.cart.views import CartCreateView, CartDetailView

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("cart/items/", CartCreateView.as_view(), name="cart-create"),
]
