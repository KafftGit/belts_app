from django.urls import path

from belts.order.views import (
    OrderCancelView,
    OrderCreateView,
    OrderDetailView,
    OrderListView,
)

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order-list"),
    path("orders/new/", OrderCreateView.as_view(), name="order-create"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("orders/<int:pk>/cancel/", OrderCancelView.as_view(), name="order-cancel"),
]
