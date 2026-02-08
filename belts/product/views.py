from django.views.generic import DetailView, ListView

from belts.product.models import Product


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.filter(available=True)


class ProductDetailView(DetailView):
    model = Product
    pk_url_kwarg = "product_id"
