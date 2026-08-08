from django.contrib import admin

from apps.finance.models.budget import Budget


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'category',
        'amount',
        'period',
        'start_date',
        'end_date',
        'alert_threshold',
    )

    list_filter = (
        'period',
        'category',
        'start_date',
    )

    search_fields = (
        'user__email',
        'category__name',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )