from django.urls import path
from belts.cart.api_views import CartDetailApiView

urlpatterns = [
    path('', CartDetailApiView.as_view(), name='api-cart-detail'),
]