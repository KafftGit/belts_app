from django.urls import path

from belts.cart.views import CartItemDeleteView, CartItemUpsertView

urlpatterns = [
    path("cart/items/", CartItemUpsertView.as_view(), name="cartitem-upsert"),
    path("cart/items/<int:pk>/delete/", CartItemDeleteView.as_view(), name="cartitem-delete"),
]
