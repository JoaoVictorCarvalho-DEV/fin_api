from rest_framework import serializers

from apps.finance.models.receipt import Receipt


class ReceiptSerializer(serializers.ModelSerializer):
    """
    Serializer para leitura de recibos e documentos.
    """

    ocr_status_display = serializers.CharField(
        source="get_ocr_status_display",
        read_only=True,
    )

    document_type_display = serializers.CharField(
        source="get_document_type_display",
        read_only=True,
    )

    is_ocr_completed = serializers.SerializerMethodField()
    is_ocr_processing = serializers.SerializerMethodField()

    class Meta:
        model = Receipt

        fields = (
            "id",
            "transaction",
            "file",
            "document_type",
            "document_type_display",
            "file_hash",
            "supplier_name",
            "supplier_document",
            "issue_date",
            "total_amount",
            "ocr_status",
            "ocr_status_display",
            "ocr_processed_at",
            "ocr_raw_text",
            "is_ocr_completed",
            "is_ocr_processing",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "file_hash",
            "supplier_name",
            "supplier_document",
            "issue_date",
            "total_amount",
            "ocr_status",
            "ocr_processed_at",
            "ocr_raw_text",
            "is_ocr_completed",
            "is_ocr_processing",
            "created_at",
            "updated_at",
        )

    def get_is_ocr_completed(self, obj):
        return obj.ocr_status == Receipt.OCRStatus.COMPLETED

    def get_is_ocr_processing(self, obj):
        return obj.ocr_status == Receipt.OCRStatus.PROCESSING


class ReceiptCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de recibos.
    """

    class Meta:
        model = Receipt

        fields = (
            "transaction",
            "file",
            "document_type",
        )

    def validate_transaction(self, transaction):
        if hasattr(transaction, "receipt"):
            raise serializers.ValidationError(
                "Esta transação já possui um recibo."
            )

        return transaction


class ReceiptUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização dos dados do recibo.
    """

    class Meta:
        model = Receipt

        fields = (
            "document_type",
        )

