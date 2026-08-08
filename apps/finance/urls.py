from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.finance.views.budget_view import BudgetViewSet
from apps.finance.views.category_view import CategoryViewSet
from apps.finance.views.financial_account_view import FinancialAccountViewSet
from apps.finance.views.receipt_view import ReceiptViewSet
from apps.finance.views.tag_view import TagViewSet
from apps.finance.views.transaction_view import TransactionViewSet


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
router.register(
    "budgets",
    BudgetViewSet,
    basename="budget"
)
router.register(
    "tags",
    TagViewSet,
    basename="tag"
)
router.register(
    "receipts",
    ReceiptViewSet,
    basename="receipt",
)
router.register(
    "transactions",
    TransactionViewSet,
    basename="transaction",
)
urlpatterns = [
    path(
        "",
        include(router.urls)
    ),
]