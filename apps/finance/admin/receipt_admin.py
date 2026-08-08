from django.contrib import admin
from django.utils.html import format_html

from apps.finance.models.receipt import Receipt
             
@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "transaction",
        "document_type",
        "supplier_name",
        "total_amount",
        "ocr_status",
        "created_at",
    )

    list_filter = (
        "document_type",
        "ocr_status",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "supplier_name",
        "supplier_document",
        "transaction__description",
        "transaction__user__email",
        "file_hash",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "file_hash",
        "ocr_processed_at",
        "ocr_raw_text",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "transaction",
    )

    list_per_page = 25

    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Documento",
            {
                "fields": (
                    "transaction",
                    "file",
                    "document_type",
                    "file_hash",
                )
            },
        ),
        (
            "Dados Extraídos",
            {
                "fields": (
                    "supplier_name",
                    "supplier_document",
                    "issue_date",
                    "total_amount",
                )
            },
        ),
        (
            "OCR",
            {
                "fields": (
                    "ocr_status",
                    "ocr_processed_at",
                    "ocr_raw_text",
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
        "mark_pending",
        "mark_processing",
        "mark_completed",
        "mark_failed",
    )
    
    @admin.display(description="Arquivo")
    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">Abrir</a>',
                obj.file.url,
            )
        return "-"

    @admin.action(description="Marcar OCR como pendente")
    def mark_pending(self, request, queryset):
        queryset.update(
            ocr_status=Receipt.OCRStatus.PENDING,
        )

    @admin.action(description="Marcar OCR como processando")
    def mark_processing(self, request, queryset):
        queryset.update(
            ocr_status=Receipt.OCRStatus.PROCESSING,
        )

    @admin.action(description="Marcar OCR como concluído")
    def mark_completed(self, request, queryset):
        queryset.update(
            ocr_status=Receipt.OCRStatus.COMPLETED,
        )

    @admin.action(description="Marcar OCR como falhou")
    def mark_failed(self, request, queryset):
        queryset.update(
            ocr_status=Receipt.OCRStatus.FAILED,
        )