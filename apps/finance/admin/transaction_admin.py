from django.contrib import admin
from apps.finance.models.transaction import Transaction

       
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "description",
        "user",
        "account",
        "category",
        "type",
        "status",
        "amount",
        "date",
        "created_at",
    )

    list_filter = (
        "type",
        "status",
        "account",
        "category",
        "date",
        "created_at",
    )

    search_fields = (
        "description",
        "notes",
        "bank_statement_id",
        "user__email",
        "account__name",
        "category__name",
    )

    ordering = (
        "-date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "related_transaction",
        "reconciled_at",
    )

    filter_horizontal = (
        "tags",
    )

    list_per_page = 25

    date_hierarchy = "date"

    autocomplete_fields = (
        "user",
        "account",
        "category",
        "related_transaction",
        "parent_transaction",
    )

    fieldsets = (
        (
            "Informações Gerais",
            {
                "fields": (
                    "user",
                    "account",
                    "category",
                    "tags",
                    "description",
                    "notes",
                )
            },
        ),
        (
            "Dados Financeiros",
            {
                "fields": (
                    "type",
                    "status",
                    "amount",
                    "date",
                )
            },
        ),
        (
            "Transferências",
            {
                "fields": (
                    "related_transaction",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
        (
            "Parcelamento",
            {
                "fields": (
                    "installment_number",
                    "total_installments",
                    "parent_transaction",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
        (
            "Conciliação Bancária",
            {
                "fields": (
                    "bank_statement_id",
                    "reconciled_at",
                ),
                "classes": (
                    "collapse",
                ),
            },
        ),
        (
            "Auditoria",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    actions = (
        "mark_completed",
        "mark_pending",
        "mark_canceled",
    )

    @admin.action(description="Marcar como concluída")
    def mark_completed(self, request, queryset):
        queryset.update(status="COMPLETED")

    @admin.action(description="Marcar como pendente")
    def mark_pending(self, request, queryset):
        queryset.update(status="PENDING")

    @admin.action(description="Marcar como cancelada")
    def mark_canceled(self, request, queryset):
        queryset.update(status="CANCELED")
      