from django.urls import include, path

urlpatterns = [
    path('users/', include('belts.user.api_urls')),
    path('products/', include('belts.product.api_urls')),
    path('cart/', include('belts.cart.api_urls')),
    path('orders/', include('belts.order.api_urls')),
]