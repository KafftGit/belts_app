from django.urls import path

from belts.cart.views import CartDetailView

urlpatterns = [
    path("cart/", CartDetailView.as_view(), name="cart"),
]
