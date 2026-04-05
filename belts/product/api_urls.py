from django.urls import path
from belts.product.api_views import ProductListApiView, ProductDetailApiView

urlpatterns = [
    path('', ProductListApiView.as_view(), name='api-product-list'),
    path('<int:pk>/', ProductDetailApiView.as_view(), name='api-product-detail'),
]