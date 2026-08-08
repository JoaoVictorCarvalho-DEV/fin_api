from django.contrib import admin

from apps.finance.models.financial_account import FinancialAccount


@admin.register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "account_type",
        "user",
        "is_active",
        "initial_balance",
        "description",
        "institution",
        "account_number",
        "agency_number",
        "credit_limit",
        "closing_day",
        "due_day",
        "updated_at",
        "created_at",
    )

    list_filter = (
        "account_type",
        "institution",
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "institution",
        "account_number",
        "agency_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    ordering = (
        "user",
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Informações Gerais",
            {
                "fields": (
                    "user",
                    "name",
                    "account_type",
                    "institution",
                    "description",
                    "is_active",
                )
            },
        ),
        (
            "Dados Bancários",
            {
                "fields": (
                    "agency_number",
                    "account_number",
                )
            },
        ),
        (
            "Valores",
            {
                "fields": (
                    "initial_balance",
                    "credit_limit",
                )
            },
        ),
        (
            "Cartão de Crédito",
            {
                "fields": (
                    "closing_day",
                    "due_day",
                )
            },
        ),
        (
            "Auditoria",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    