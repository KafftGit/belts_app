from django.views.decorators.http import require_http_methods

from belts.user.manager import UserViewManager


@require_http_methods(["GET", "POST"])
def login_view(request):
    return UserViewManager.login(request)


@require_http_methods(["GET", "POST"])
def logout_view(request):
    return UserViewManager.logout(request)


@require_http_methods(["GET", "POST"])
def register_view(request):
    return UserViewManager.register(request)
