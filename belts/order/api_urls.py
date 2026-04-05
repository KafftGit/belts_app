from django.urls import path
from belts.order.api_views import OrderListApiView, OrderDetailApiView, OrderCreateApiView

urlpatterns = [
    path('', OrderListApiView.as_view(), name='api-order-list'),
    path('create/', OrderCreateApiView.as_view(), name='api-order-create'),
    path('<int:pk>/', OrderDetailApiView.as_view(), name='api-order-detail'),
]