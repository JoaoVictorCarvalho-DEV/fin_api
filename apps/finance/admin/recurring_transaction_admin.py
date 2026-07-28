from django.contrib import admin

from apps.finance.models.recurring_transaction import RecurringTransaction


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "description",
        "user",
        "account",
        "category",
        "transaction_type",
        "amount",
        "frequency",
        "next_execution",
        "is_active",
    )

    list_filter = (
        "transaction_type",
        "frequency",
        "is_active",
        "category",
        "created_at",
    )

    search_fields = (
        "description",
        "user__email",
        "user__first_name",
        "user__last_name",
        "account__name",
        "category__name",
    )

    ordering = (
        "next_execution",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "user",
        "account",
        "category",
    )

    fieldsets = (
        (
            "Informações Gerais",
            {
                "fields": (
                    "user",
                    "description",
                    "transaction_type",
                    "amount",
                    "notes",
                )
            },
        ),
        (
            "Relacionamentos",
            {
                "fields": (
                    "account",
                    "category",
                )
            },
        ),
        (
            "Recorrência",
            {
                "fields": (
                    "frequency",
                    "start_date",
                    "end_date",
                    "next_execution",
                    "is_active",
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