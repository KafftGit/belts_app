from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import DetailView, ListView

from belts.order.models import Order, Status
from mixins import IsUserOwnerOfModelMixin


class OrderDetailView(IsUserOwnerOfModelMixin, DetailView):
    model = Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    paginate_by = 8

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")


class OrderCreateView(LoginRequiredMixin, View):
    pass


class OrderCancelView(IsUserOwnerOfModelMixin, View):

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk)

        order.status = Status.CANCELED
        order.save()
        return JsonResponse({}, status=200)
