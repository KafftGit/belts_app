from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# =========================
# Регистрация
# =========================
class RegisterApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Регистрация пользователя",
        operation_description="Создаёт нового пользователя",
        tags=["Users"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            201: openapi.Response(
                description="Пользователь создан",
                examples={
                    "application/json": {
                        "message": "Пользователь успешно зарегистрирован"
                    }
                },
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"detail": "Все поля обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(password) < 8:
            return Response(
                {"detail": "Пароль должен быть не менее 8 символов"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password.isdigit():
            return Response(
                {"detail": "Пароль не должен состоять только из цифр"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"detail": "Пользователь уже существует"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password)

        return Response(
            {"message": "Пользователь успешно зарегистрирован"},
            status=status.HTTP_201_CREATED
        )


# =========================
# Логин
# =========================
class LoginApiView(APIView):
    @swagger_auto_schema(
        operation_summary="Авторизация пользователя",
        operation_description="Вход пользователя в систему",
        tags=["Users"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            200: openapi.Response(
                description="Успешный вход",
                examples={
                    "application/json": {
                        "message": "Успешная авторизация"
                    }
                },
            ),
            401: "Неверные данные",
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Неверный логин или пароль"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)

        return Response(
            {"message": "Успешная авторизация"},
            status=status.HTTP_200_OK
        )


# =========================
# Текущий пользователь
# =========================
class CurrentUserApiView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение текущего пользователя",
        operation_description="Возвращает данные авторизованного пользователя",
        tags=["Users"],
        responses={
            200: openapi.Response(
                description="Данные пользователя",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "test_user"
                    }
                },
            ),
            401: "Не авторизован",
        },
    )
    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "username": user.username,
            },
            status=status.HTTP_200_OK
        )