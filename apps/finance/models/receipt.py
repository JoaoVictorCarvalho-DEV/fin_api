from decimal import Decimal
from datetime import datetime

from django.core.validators import MinValueValidator
from django.db import models

from apps.finance.models.transaction import Transaction


def receipt_upload_path(instance, filename):
    today = datetime.now()

    return (
        f"receipts/"
        f"{instance.transaction.user.id}/"
        f"{today:%Y/%m}/"
        f"{filename}"
    )


class Receipt(models.Model):
    """
    Recibos e documentos anexados às transações.
    """

    class OCRStatus(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        PROCESSING = "PROCESSING", "Processando"
        COMPLETED = "COMPLETED", "Concluído"
        FAILED = "FAILED", "Falha"

    class DocumentType(models.TextChoices):
        RECEIPT = "RECEIPT", "Recibo"
        INVOICE = "INVOICE", "Nota Fiscal"
        OTHER = "OTHER", "Outro"

    # Relacionamentos

    transaction = models.OneToOneField(
        Transaction,
        verbose_name="Transação",
        on_delete=models.CASCADE,
        related_name="receipt",
    )

    # Arquivo

    file = models.FileField(
        "Arquivo",
        upload_to=receipt_upload_path,
    )

    file_hash = models.CharField(
        "Hash do Arquivo",
        max_length=64,
        unique=True,
        blank=True,
    )

    document_type = models.CharField(
        "Tipo do Documento",
        max_length=20,
        choices=DocumentType.choices,
        default=DocumentType.RECEIPT,
    )

    # Dados extraídos pelo OCR

    supplier_name = models.CharField(
        "Fornecedor",
        max_length=200,
        blank=True,
    )

    supplier_document = models.CharField(
        "Documento do Fornecedor",
        max_length=20,
        blank=True,
    )

    issue_date = models.DateField(
        "Data de Emissão",
        null=True,
        blank=True,
    )

    total_amount = models.DecimalField(
        "Valor Total",
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("0.01"))
        ],
    )

    # Controle do OCR

    ocr_status = models.CharField(
        "Status do OCR",
        max_length=20,
        choices=OCRStatus.choices,
        default=OCRStatus.PENDING,
    )

    ocr_processed_at = models.DateTimeField(
        "Processado em",
        null=True,
        blank=True,
    )

    ocr_raw_text = models.TextField(
        "Texto OCR Bruto",
        blank=True,
    )

    # Auditoria

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"

        indexes = [
            models.Index(fields=["transaction"]),
            models.Index(fields=["ocr_status"]),
            models.Index(fields=["supplier_name"]),
            models.Index(fields=["ocr_status", "created_at"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_amount__gte=0),
                name="receipt_total_amount_positive",
            ),
        ]

    def __str__(self):
        return f"Recibo #{self.pk} - {self.transaction.description}"

    @property
    def is_ocr_completed(self):
        return self.ocr_status == self.OCRStatus.COMPLETED

    @property
    def is_ocr_processing(self):
        return self.ocr_status == self.OCRStatus.PROCESSING

    @property
    def is_ocr_failed(self):
        return self.ocr_status == self.OCRStatus.FAILED

    @property
    def is_ocr_pending(self):
        return self.ocr_status == self.OCRStatus.PENDING