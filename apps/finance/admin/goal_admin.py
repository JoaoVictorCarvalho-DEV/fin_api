from django.contrib import admin

from apps.finance.models.goal import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "status",
        "target_amount",
        "saved_amount",
        "priority",
        "target_date",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "category",
        "created_at",
    )

    search_fields = (
        "name",
        "user__email",
        "user__first_name",
        "user__last_name",
        "category__name",
    )

    ordering = (
        "-priority",
        "target_date",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "user",
        "category",
        "related_account",
    )

    fieldsets = (
        (
            "Informações Gerais",
            {
                "fields": (
                    "user",
                    "name",
                    "description",
                    "status",
                    "priority",
                )
            },
        ),
        (
            "Valores",
            {
                "fields": (
                    "target_amount",
                    "saved_amount",
                )
            },
        ),
        (
            "Período",
            {
                "fields": (
                    "start_date",
                    "target_date",
                )
            },
        ),
        (
            "Relacionamentos",
            {
                "fields": (
                    "category",
                    "related_account",
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