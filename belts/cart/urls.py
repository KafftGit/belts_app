# from django.urls import path

# from belts.cart.views import CartCompleteView, CartCreateView, CartDetailView, CartItemView

# urlpatterns = [
#     path("cart/", CartDetailView.as_view(), name="cart"),
#     path("cart/items/", CartCreateView.as_view(), name="cart-create"),
#     path("cart/items/delete/", CartItemView.as_view(), name="cart-item-delete"),
#     path("cart/complete/", CartCompleteView.as_view(), name="cart-complete"),
# ]
from django.urls import path

from belts.cart.views import (
    CartCompleteView,
    CartCreateView,
    CartDetailView,
    CartItemChangeView,
    CartItemUpdateView,
    CartItemView,
)

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart"),
    path("cart/items/", CartCreateView.as_view(), name="cart-create"),
    path("cart/items/update/", CartItemUpdateView.as_view(), name="cart-item-update"),
    path("cart/items/change/", CartItemChangeView.as_view(), name="cart-item-change"),
    path("cart/items/delete/", CartItemView.as_view(), name="cart-item-delete"),
    path("cart/complete/", CartCompleteView.as_view(), name="cart-complete"),
]