from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from belts.product.models import Product


class ProductListApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение списка товаров",
        operation_description="Возвращает список товаров интернет-магазина Fabis Craft.",
        tags=["Products"],
        responses={
            200: openapi.Response(
                description="Список товаров успешно получен",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "name": "Ремень классический",
                            "price": "3500.00",
                        }
                    ]
                },
            )
        },
    )
    def get(self, request):
        products = Product.objects.all()

        data = []
        for product in products:
            data.append({
                "id": product.id,
                "name": getattr(product, "name", ""),
                "price": str(getattr(product, "price", "")),
            })

        return Response(data, status=status.HTTP_200_OK)


class ProductDetailApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Получение товара по ID",
        operation_description="Возвращает детальную информацию о выбранном товаре.",
        tags=["Products"],
        responses={
            200: openapi.Response(
                description="Данные товара успешно получены",
                examples={
                    "application/json": {
                        "id": 1,
                        "name": "Ремень классический",
                        "price": "3500.00",
                    }
                },
            ),
            404: openapi.Response(
                description="Товар не найден",
                examples={
                    "application/json": {
                        "detail": "Товар не найден"
                    }
                },
            ),
        },
    )
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "id": product.id,
            "name": getattr(product, "name", ""),
            "price": str(getattr(product, "price", "")),
        }
        return Response(data, status=status.HTTP_200_OK)
