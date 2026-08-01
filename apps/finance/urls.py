from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.finance.views.category_view import CategoryViewSet
from apps.finance.views.financial_account_view import FinancialAccountViewSet


router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category"
)
router.register(
    "accounts",
    FinancialAccountViewSet,
    basename="financial-account"
)

urlpatterns = [
    path(
        "",
        include(router.urls)
    ),
]