from django.urls import path
from belts.user.api_views import RegisterApiView, LoginApiView, CurrentUserApiView

urlpatterns = [
    path('register/', RegisterApiView.as_view(), name='api-user-register'),
    path('login/', LoginApiView.as_view(), name='api-user-login'),
    path('profile/', CurrentUserApiView.as_view(), name='api-user-profile'),
]