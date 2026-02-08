from django.views.generic import DetailView, ListView

from belts.product.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "home.html"
    paginate_by = 4

    def get_queryset(self):
        return Product.objects.filter(available=True).prefetch_related("images").order_by("name")


class ProductDetailView(DetailView):
    model = Product
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "product/detail.html"
