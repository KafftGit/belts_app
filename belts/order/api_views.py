from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from belts.order.models import Order


class OrderListApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение списка заказов",
        operation_description="Возвращает список заказов текущего пользователя.",
        tags=["Orders"],
        responses={
            200: openapi.Response(
                description="Список заказов успешно получен",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "status": "NEW",
                            "total_price": "13900.00",
                            "address": "Москва, ул. Пушкина, д. 10, кв. 5",
                            "recipient_name": "Иван Иванов",
                            "phone": "+7 (999) 123-45-67",
                            "created_at": "2026-04-03T20:00:00"
                        }
                    ]
                },
            ),
            401: openapi.Response(
                description="Требуется авторизация",
                examples={
                    "application/json": {
                        "detail": "Требуется авторизация"
                    }
                },
            ),
        },
    )
    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("items", "items__product")

        data = []
        for order in orders:
            data.append({
                "id": order.id,
                "status": order.status,
                "total_price": str(order.total_price),
                "address": order.address,
                "recipient_name": order.recipient_name,
                "phone": order.phone,
                "created_at": order.created_at.isoformat() if order.created_at else None,
            })

        return Response(data, status=status.HTTP_200_OK)


class OrderDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение заказа",
        operation_description="Возвращает подробную информацию о выбранном заказе.",
        tags=["Orders"],
        responses={
            200: openapi.Response(
                description="Заказ успешно получен",
                examples={
                    "application/json": {
                        "id": 1,
                        "status": "NEW",
                        "total_price": "13900.00",
                        "recipient_name": "Иван Иванов",
                        "phone": "+7 (999) 123-45-67",
                        "city": "Москва",
                        "street": "Пушкина",
                        "house": "10",
                        "apartment": "5",
                        "entrance": "2",
                        "floor": "3",
                        "intercom": "45",
                        "postal_code": "101000",
                        "address": "Москва, ул. Пушкина, д. 10, кв. 5",
                        "extra_notes": "Позвонить перед доставкой",
                        "created_at": "2026-04-03T20:00:00",
                        "items": [
                            {
                                "product_id": 2,
                                "product_name": "Автобокс «Бордовая снежинка»",
                                "quantity": 2,
                                "unit_price": "6950.00",
                                "total_price": "13900.00"
                            }
                        ]
                    }
                },
            ),
            401: openapi.Response(
                description="Требуется авторизация",
                examples={
                    "application/json": {
                        "detail": "Требуется авторизация"
                    }
                },
            ),
            404: openapi.Response(
                description="Заказ не найден",
                examples={
                    "application/json": {
                        "detail": "Заказ не найден"
                    }
                },
            ),
        },
    )
    def get(self, request, pk):
        try:
            order = Order.objects.prefetch_related("items", "items__product").get(pk=pk, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Заказ не найден"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "id": order.id,
            "status": order.status,
            "total_price": str(order.total_price),
            "recipient_name": order.recipient_name,
            "phone": order.phone,
            "city": order.city,
            "street": order.street,
            "house": order.house,
            "apartment": order.apartment,
            "entrance": order.entrance,
            "floor": order.floor,
            "intercom": order.intercom,
            "postal_code": order.postal_code,
            "address": order.address,
            "extra_notes": order.extra_notes,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "items": [],
        }

        for item in order.items.all():
            data["items"].append({
                "product_id": item.product.id,
                "product_name": getattr(item.product, "name", ""),
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "total_price": str(item.total_price),
            })

        return Response(data, status=status.HTTP_200_OK)