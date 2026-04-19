from django.urls import path

from belts.cart.api_views import (
    CartCompleteApiView,
    CartDetailApiView,
    CartItemChangeApiView,
    CartItemCreateApiView,
    CartItemDeleteApiView,
    CartItemUpdateApiView,
)

urlpatterns = [
    path("", CartDetailApiView.as_view(), name="api-cart-detail"),
    path("items/", CartItemCreateApiView.as_view(), name="api-cart-create"),
    path("items/update/", CartItemUpdateApiView.as_view(), name="api-cart-update"),
    path("items/change/", CartItemChangeApiView.as_view(), name="api-cart-change"),
    path("items/delete/", CartItemDeleteApiView.as_view(), name="api-cart-delete"),
    path("complete/", CartCompleteApiView.as_view(), name="api-cart-complete"),
]