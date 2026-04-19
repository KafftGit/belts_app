from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import DetailView, ListView

from belts.mixins import IsUserOwnerOfModelMixin
from belts.order.manager import OrderViewManager
from belts.order.models import Order


class OrderDetailView(IsUserOwnerOfModelMixin, DetailView):
    model = Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 8

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderCreateView(LoginRequiredMixin, View):
    def post(self, request):
        return OrderViewManager.create(request)


class OrderCancelView(IsUserOwnerOfModelMixin, DetailView):
    model = Order

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.status = "CANCELLED"
        self.object.save(update_fields=["status"])

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)