from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


class UserViewManager:
    @staticmethod
    def login(request):
        if request.method == "GET":
            return render(request, "user/login.html")

        username, password = request.POST.get("username"), request.POST.get("password")
        if not username or not password:
            return render(
                request,
                "user/login.html",
                {"error": "Имя пользователя и пароль обязательны"},
                status=400,
            )

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, "user/login.html", {"error": "Invalid credentials."}, status=401)

        login(request, user)
        return redirect("home-page")

    @staticmethod
    def logout(request):
        if request.method == "POST":
            logout(request)
            return redirect("home-page")

        return render(request, "user/logout.html")

    @staticmethod
    def register(request):
        if request.method == "GET":
            return render(request, "user/register.html")

        payload = request.POST

        username = payload.get("username", "").strip()
        password = payload.get("password")
        confirm_password = payload.get("confirm_password")
        email = payload.get("email", "").strip()

        if not username or not password:
            error = "Имя пользователя и пароль обязательны"
            return render(request, "user/register.html", {"error": error}, status=400)

        if confirm_password is not None and password != confirm_password:
            error = "Пароли не совпадают"
            return render(request, "user/register.html", {"error": error}, status=400)

        if User.objects.filter(username=username).exists():
            error = "Такое имя пользователя уже существует"
            return render(request, "user/register.html", {"error": error}, status=409)

        User.objects.create_user(username=username, password=password, email=email)

        return redirect("home-page")
