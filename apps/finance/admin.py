from django.contrib import admin

from apps.finance.models.category import Category
from apps.finance.models.financial_account import FinancialAccount
from apps.finance.models.tag import Tag
from apps.finance.models.transaction import Transaction

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
    
@admin.register(FinancialAccount)
class FinancialAccountAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
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
        "type",
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
        "current_balance",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Informações Gerais",
            {
                "fields": (
                    "user",
                    "name",
                    "type",
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
                    "current_balance",
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
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "user",
        "color",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    ordering = (
        "name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 25

    fieldsets = (
        (
            "Informações da Tag",
            {
                "fields": (
                    "user",
                    "name",
                    "color",
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

    actions = (
        "activate_tags",
        "deactivate_tags",
    )

    @admin.action(description="Ativar tags selecionadas")
    def activate_tags(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Desativar tags selecionadas")
    def deactivate_tags(self, request, queryset):
        queryset.update(is_active=False)
        
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