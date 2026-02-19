from django.urls import path

from belts.cart.views import CartCreateView, CartDetailView, CartItemView

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("cart/items/", CartCreateView.as_view(), name="cart-create"),
    path("cart/items/delete/", CartItemView.as_view(), name="cart-item-delete"),
]
