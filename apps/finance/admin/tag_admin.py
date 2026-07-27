from django.contrib import admin

from apps.finance.models.tag import Tag

 
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
   