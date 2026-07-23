from django.urls import path

from apps.accounts.views.register import RegisterView
from apps.accounts.views.login import LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view(), name="login"),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    #GET path("me/", MeView.as_view()),
    #PATCH path("me/", MeView.as_view()),
    #POST path("change-password/", ChangePasswordView.as_view()),
    #POST path("logout/", LogoutView.as_view()),
]