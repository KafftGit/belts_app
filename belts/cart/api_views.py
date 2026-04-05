from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from belts.cart.models import Cart, CartItem


class CartDetailApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение корзины пользователя",
        operation_description="Возвращает содержимое корзины текущего пользователя.",
        tags=["Cart"],
        responses={
            200: openapi.Response(
                description="Корзина успешно получена",
                examples={
                    "application/json": {
                        "cart_id": 1,
                        "items": [
                            {
                                "product_id": 2,
                                "product_name": "Автобокс «Бордовая снежинка»",
                                "quantity": 2,
                                "unit_price": "6950.00",
                                "total_price": "13900.00"
                            }
                        ],
                        "total_price": "13900.00"
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
        },
    )
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Требуется авторизация"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = CartItem.objects.filter(cart=cart).select_related("product")

        data = {
            "cart_id": cart.id,
            "items": [],
            "total_price": "0.00",
        }

        total = 0
        for item in items:
            item_total = item.unit_price * item.quantity
            total += item_total
            data["items"].append({
                "product_id": item.product.id,
                "product_name": getattr(item.product, "name", ""),
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "total_price": str(item_total),
            })

        data["total_price"] = str(total)
        return Response(data, status=status.HTTP_200_OK)