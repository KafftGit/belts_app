from decimal import Decimal

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from belts.cart.models import Cart, CartItem
from belts.cart.serializers import (
    CartCompleteSerializer,
    CartItemChangeSerializer,
    CartItemCreateSerializer,
    CartItemDeleteSerializer,
    CartItemUpdateSerializer,
)
from belts.order.models import Order, OrderItem
from belts.product.models import Product


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
                                "total_price": "13900.00",
                                "stock": 5,
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

        total = Decimal("0.00")
        for item in items:
            item_total = item.unit_price * item.quantity
            total += item_total
            data["items"].append({
                "product_id": item.product.id,
                "product_name": getattr(item.product, "name", ""),
                "quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "total_price": str(item_total),
                "stock": item.product.stock,
            })

        data["total_price"] = str(total)
        return Response(data, status=status.HTTP_200_OK)


class CartItemCreateApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Добавление товара в корзину",
        operation_description="Добавляет товар в корзину или увеличивает его количество, если товар уже есть.",
        tags=["Cart"],
        request_body=CartItemCreateSerializer,
        responses={
            201: openapi.Response(
                description="Товар добавлен в корзину",
                examples={
                    "application/json": {
                        "product_id": 2,
                        "item_quantity": 2,
                        "unit_price": "6950.00",
                        "item_total_price": "13900.00",
                        "cart_total_price": "13900.00",
                        "stock": 5,
                    }
                },
            ),
            400: openapi.Response(
                description="Ошибка валидации или недостаточно товара на складе",
                examples={
                    "application/json": {
                        "detail": "В наличии только 3 шт. товара"
                    }
                },
            ),
            401: "Требуется авторизация",
            404: "Товар не найден",
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartItemCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data["product"]
        quantity_to_add = serializer.validated_data["quantity"]

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Товар не найден"}, status=status.HTTP_404_NOT_FOUND)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            item = CartItem.objects.get(cart=cart, product=product)
            new_quantity = item.quantity + quantity_to_add

            if new_quantity > product.stock:
                return Response(
                    {"detail": f"В наличии только {product.stock} шт. товара"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item.quantity = new_quantity
            item.unit_price = product.price
            item.save(update_fields=["quantity", "unit_price"])
        except CartItem.DoesNotExist:
            if quantity_to_add > product.stock:
                return Response(
                    {"detail": f"В наличии только {product.stock} шт. товара"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity_to_add,
                unit_price=product.price,
            )

        cart_total = sum(i.unit_price * i.quantity for i in cart.items.all())

        return Response(
            {
                "product_id": product.id,
                "item_quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "item_total_price": str(item.unit_price * item.quantity),
                "cart_total_price": str(cart_total),
                "stock": product.stock,
            },
            status=status.HTTP_201_CREATED,
        )


class CartItemUpdateApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Установка количества товара в корзине",
        operation_description="Устанавливает точное количество товара в корзине.",
        tags=["Cart"],
        request_body=CartItemUpdateSerializer,
        responses={
            200: openapi.Response(
                description="Количество товара обновлено",
                examples={
                    "application/json": {
                        "product_id": 2,
                        "item_quantity": 3,
                        "unit_price": "6950.00",
                        "item_total_price": "20850.00",
                        "cart_total_price": "20850.00",
                        "stock": 5,
                    }
                },
            ),
            400: "Ошибка валидации или недостаточно товара на складе",
            401: "Требуется авторизация",
            404: "Товар не найден в корзине",
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartItemUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            item = CartItem.objects.select_related("product").get(
                cart=cart,
                product_id=serializer.validated_data["product"],
            )
        except CartItem.DoesNotExist:
            return Response({"detail": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.validated_data["quantity"] > item.product.stock:
            return Response(
                {"detail": f"В наличии только {item.product.stock} шт. товара"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item.quantity = serializer.validated_data["quantity"]
        item.save(update_fields=["quantity"])

        cart_total = sum(i.unit_price * i.quantity for i in cart.items.all())

        return Response(
            {
                "product_id": item.product_id,
                "item_quantity": item.quantity,
                "unit_price": str(item.unit_price),
                "item_total_price": str(item.unit_price * item.quantity),
                "cart_total_price": str(cart_total),
                "stock": item.product.stock,
            },
            status=status.HTTP_200_OK,
        )


class CartItemChangeApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Изменение количества товара кнопками + и -",
        operation_description=(
            "Увеличивает или уменьшает количество товара в корзине на 1. "
            "Если quantity = 1 и action = decrease, товар удаляется из корзины."
        ),
        tags=["Cart"],
        request_body=CartItemChangeSerializer,
        responses={
            200: openapi.Response(
                description="Количество товара изменено",
                examples={
                    "application/json": {
                        "product_id": 2,
                        "removed": False,
                        "item_quantity": 2,
                        "unit_price": "6950.00",
                        "item_total_price": "13900.00",
                        "cart_total_price": "13900.00",
                        "stock": 5,
                    }
                },
            ),
            400: "Некорректные данные или недостаточно товара на складе",
            401: "Требуется авторизация",
            404: "Товар не найден в корзине",
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartItemChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_id = serializer.validated_data["product"]
        action = serializer.validated_data["action"]

        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            item = CartItem.objects.select_related("product").get(
                cart=cart,
                product_id=product_id,
            )
        except CartItem.DoesNotExist:
            return Response({"detail": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        if action == "increase":
            if item.quantity + 1 > item.product.stock:
                return Response(
                    {"detail": f"В наличии только {item.product.stock} шт. товара"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            item.quantity += 1
            item.save(update_fields=["quantity"])
            removed = False
        else:
            if item.quantity > 1:
                item.quantity -= 1
                item.save(update_fields=["quantity"])
                removed = False
            else:
                item.delete()
                removed = True

        cart_total = sum(i.unit_price * i.quantity for i in cart.items.all())

        return Response(
            {
                "product_id": product_id,
                "removed": removed,
                "item_quantity": None if removed else item.quantity,
                "unit_price": None if removed else str(item.unit_price),
                "item_total_price": None if removed else str(item.unit_price * item.quantity),
                "cart_total_price": str(cart_total),
                "stock": None if removed else item.product.stock,
            },
            status=status.HTTP_200_OK,
        )


class CartItemDeleteApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Удаление товара из корзины",
        operation_description="Удаляет выбранный товар из корзины пользователя.",
        tags=["Cart"],
        request_body=CartItemDeleteSerializer,
        responses={
            200: openapi.Response(
                description="Товар удалён из корзины",
                examples={
                    "application/json": {
                        "product_id": 2,
                        "removed": True,
                        "cart_total_price": "0.00"
                    }
                },
            ),
            401: "Требуется авторизация",
            404: "Товар не найден в корзине",
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartItemDeleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        try:
            item = CartItem.objects.get(
                cart=cart,
                product_id=serializer.validated_data["product"],
            )
        except CartItem.DoesNotExist:
            return Response({"detail": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        product_id = item.product_id
        item.delete()
        cart_total = sum(i.unit_price * i.quantity for i in cart.items.all())

        return Response(
            {
                "product_id": product_id,
                "removed": True,
                "cart_total_price": str(cart_total),
            },
            status=status.HTTP_200_OK,
        )


class CartCompleteApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Оформление заказа",
        operation_description="Создаёт заказ из текущей корзины пользователя.",
        tags=["Cart"],
        request_body=CartCompleteSerializer,
        responses={
            201: openapi.Response(
                description="Заказ успешно оформлен",
                examples={"application/json": {"id": 15}},
            ),
            400: openapi.Response(
                description="Ошибка валидации, корзина пуста или недостаточно товара",
                examples={
                    "application/json": {
                        "detail": "Недостаточно товара «Название товара». В наличии: 2"
                    }
                },
            ),
            401: "Требуется авторизация",
        },
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CartCompleteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        items = CartItem.objects.filter(cart__user=request.user).select_related("product")

        if not items.exists():
            return Response({"detail": "Корзина пуста"}, status=status.HTTP_400_BAD_REQUEST)

        for item in items:
            if item.quantity > item.product.stock:
                return Response(
                    {"detail": f"Недостаточно товара «{item.product.name}». В наличии: {item.product.stock}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        order_total_price = sum(item.unit_price * item.quantity for item in items)

        full_address_parts = [
            serializer.validated_data["city"],
            f"ул. {serializer.validated_data['street']}",
            f"д. {serializer.validated_data['house']}",
            f"кв. {serializer.validated_data['apartment']}" if serializer.validated_data.get("apartment") else "",
            f"подъезд {serializer.validated_data['entrance']}" if serializer.validated_data.get("entrance") else "",
            f"этаж {serializer.validated_data['floor']}" if serializer.validated_data.get("floor") else "",
            f"домофон {serializer.validated_data['intercom']}" if serializer.validated_data.get("intercom") else "",
        ]
        full_address = ", ".join([part for part in full_address_parts if part])

        order = Order.objects.create(
            user=request.user,
            total_price=order_total_price,
            recipient_name=serializer.validated_data["recipient_name"],
            phone=serializer.validated_data["phone"],
            city=serializer.validated_data["city"],
            street=serializer.validated_data["street"],
            house=serializer.validated_data["house"],
            apartment=serializer.validated_data.get("apartment", ""),
            entrance=serializer.validated_data.get("entrance", ""),
            floor=serializer.validated_data.get("floor", ""),
            intercom=serializer.validated_data.get("intercom", ""),
            postal_code=serializer.validated_data.get("postal_code", ""),
            address=full_address,
            extra_notes=serializer.validated_data.get("extra_notes", ""),
        )

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.unit_price * item.quantity,
                )
                for item in items
            ]
        )

        for item in items:
            product = item.product
            product.stock -= item.quantity
            product.save(update_fields=["stock"])

        items.delete()

        return Response({"id": order.id}, status=status.HTTP_201_CREATED)