from django.contrib import admin

from apps.finance.models.recurring_transaction import RecurringTransaction


@admin.register(RecurringTransaction)
class RecurringTransactionAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "frequency",
        "start_date",
        "next_execution",
        "is_active",
        "created_at",
    )

    list_filter = (
        "frequency",
        "is_active",
        "created_at",
    )

    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
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
    )

    fieldsets = (
        (
            "Informações Gerais",
            {
                "fields": (
                    "user",
                    "frequency",
                    "is_active",
                )
            },
        ),
        (
            "Template da Transação",
            {
                "fields": (
                    "transaction_template",
                )
            },
        ),
        (
            "Agendamento",
            {
                "fields": (
                    "start_date",
                    "end_date",
                    "next_execution",
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