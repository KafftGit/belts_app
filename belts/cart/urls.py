from django.urls import path

from belts.cart.views import CartCompleteView, CartCreateView, CartDetailView, CartItemView

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("cart/items/", CartCreateView.as_view(), name="cart-create"),
    path("cart/items/delete/", CartItemView.as_view(), name="cart-item-delete"),
    path("cart/complete/", CartCompleteView.as_view(), name="cart-complete"),
]
