from django.urls import path
from apps.finance.views.category import (
    CategoryDetailView,
    CategoryListCreateView,
)

urlpatterns = [
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),

    path(
        "categories/<int:category_id>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
]