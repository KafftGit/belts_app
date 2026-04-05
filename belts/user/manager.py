from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from belts.user.forms import UserLoginForm, UserRegisterForm


class UserViewManager:

    @staticmethod
    def login(request):
        if request.method == "GET":
            return render(request, "user/login.html", {"form": UserLoginForm()})

        form = UserLoginForm(request, data=request.POST)
        if not form.is_valid():
            return render(request, "user/login.html", {"form": form}, status=401)

        login(request, form.get_user())
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
            return render(request, "user/register.html", {"form": UserRegisterForm()})

        form = UserRegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "user/register.html", {"form": form}, status=400)

        login(request, form.save())

        return redirect("home-page")

