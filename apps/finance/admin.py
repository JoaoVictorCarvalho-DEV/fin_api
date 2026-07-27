from django.contrib import admin

from apps.finance.models.category import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "user",
        "is_active",
        "created_at",
    )

    list_filter = (
        "type",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
        "user__email",
    )

    ordering = (
        "type",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )