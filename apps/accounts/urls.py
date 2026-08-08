from django.urls import path

from apps.accounts.views.change_password import ChangePasswordView
from apps.accounts.views.register import RegisterView
from apps.accounts.views.login import LoginView
from apps.accounts.views.me import MeView
from apps.accounts.views.logout import LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
]