from django.urls import path

from belts.product.views import ProductDetailView, ProductListView

urlpatterns = [
    path("", ProductListView.as_view(), name="home-page"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]
