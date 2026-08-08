import hashlib

from django.db import transaction

from apps.finance.models.receipt import Receipt
from apps.finance.models.transaction import Transaction

from apps.finance.exceptions.receipt_exceptions import (
    ReceiptNotFoundError,
    ReceiptAlreadyExistsError,
    ReceiptFileRequiredError,
    ReceiptFileAlreadyExistsError,
    OCRProcessingError,
    OCRAlreadyProcessingError,
    OCRNotCompletedError,
)


class ReceiptService:
    """
    Regras de negócio relacionadas aos recibos e documentos.
    """

    @staticmethod
    def _calculate_file_hash(file):
        """
        Calcula o SHA-256 do arquivo.
        """

        sha256 = hashlib.sha256()

        for chunk in file.chunks():
            sha256.update(chunk)

        file.seek(0)

        return sha256.hexdigest()

    @staticmethod
    def create(user, validated_data):
        """
        Cria um novo recibo para uma transação do usuário.
        """

        file = validated_data.get("file")

        if not file:
            raise ReceiptFileRequiredError()

        transaction_obj = validated_data["transaction"]

        # Garante que a transação pertence ao usuário.
        if transaction_obj.user_id != user.id:
            raise ReceiptNotFoundError()

        # Uma transação só pode possuir um recibo.
        if Receipt.objects.filter(
            transaction=transaction_obj
        ).exists():

            raise ReceiptAlreadyExistsError(
                transaction_obj.id
            )

        # Calcula o hash antes de salvar.
        file_hash = ReceiptService._calculate_file_hash(
            file
        )

        # Evita documentos duplicados.
        if Receipt.objects.filter(
            file_hash=file_hash
        ).exists():

            raise ReceiptFileAlreadyExistsError()

        with transaction.atomic():

            receipt = Receipt.objects.create(
                file_hash=file_hash,
                **validated_data,
            )

        return receipt

    @staticmethod
    def get_by_id(user, receipt_id):
        """
        Busca um recibo pertencente a uma transação do usuário.
        """

        try:

            return Receipt.objects.select_related(
                "transaction",
                "transaction__user",
            ).get(
                id=receipt_id,
                transaction__user=user,
            )

        except Receipt.DoesNotExist:

            raise ReceiptNotFoundError(
                receipt_id
            )

    @staticmethod
    def list(user):
        """
        Lista todos os recibos pertencentes ao usuário.
        """

        return Receipt.objects.filter(
            transaction__user=user,
        ).select_related(
            "transaction",
        ).order_by(
            "-created_at"
        )

    @staticmethod
    def update(receipt, validated_data):
        """
        Atualiza os dados permitidos de um recibo.

        Os dados extraídos pelo OCR não devem ser
        alterados diretamente pelo usuário.
        """

        for field, value in validated_data.items():

            setattr(
                receipt,
                field,
                value,
            )

        receipt.full_clean()

        receipt.save()

        return receipt

    @staticmethod
    def delete(receipt):
        """
        Exclui um recibo e seu arquivo associado.
        """

        file = receipt.file

        with transaction.atomic():

            receipt.delete()

            if file:
                file.delete(
                    save=False
                )

        return True

    @staticmethod
    def start_ocr(receipt):
        """
        Marca o recibo como aguardando processamento OCR.

        O processamento efetivo será realizado
        posteriormente pelo OCRService/tarefa assíncrona.
        """

        if receipt.ocr_status == Receipt.OCRStatus.PROCESSING:

            raise OCRAlreadyProcessingError()

        if receipt.ocr_status == Receipt.OCRStatus.COMPLETED:

            raise OCRProcessingError(
                "O OCR deste recibo já foi concluído."
            )

        receipt.ocr_status = Receipt.OCRStatus.PROCESSING
        receipt.ocr_processed_at = None

        receipt.save(
            update_fields=[
                "ocr_status",
                "ocr_processed_at",
                "updated_at",
            ]
        )

        return receipt

    @staticmethod
    def complete_ocr(
        receipt,
        supplier_name=None,
        supplier_document=None,
        issue_date=None,
        total_amount=None,
        raw_text="",
    ):
        """
        Finaliza o processamento OCR e salva
        os dados extraídos.
        """

        if receipt.ocr_status != Receipt.OCRStatus.PROCESSING:

            raise OCRProcessingError(
                "O recibo não está em processamento."
            )

        receipt.supplier_name = supplier_name or ""
        receipt.supplier_document = supplier_document or ""
        receipt.issue_date = issue_date
        receipt.total_amount = total_amount
        receipt.ocr_raw_text = raw_text or ""
        receipt.ocr_status = Receipt.OCRStatus.COMPLETED
        receipt.ocr_processed_at = receipt.updated_at

        receipt.full_clean()

        receipt.save(
            update_fields=[
                "supplier_name",
                "supplier_document",
                "issue_date",
                "total_amount",
                "ocr_raw_text",
                "ocr_status",
                "ocr_processed_at",
                "updated_at",
            ]
        )

        return receipt

    @staticmethod
    def fail_ocr(receipt, error_message=None):
        """
        Marca o processamento OCR como falho.
        """

        receipt.ocr_status = Receipt.OCRStatus.FAILED

        receipt.save(
            update_fields=[
                "ocr_status",
                "updated_at",
            ]
        )

        return receipt

    @staticmethod
    def require_completed_ocr(receipt):
        """
        Garante que o OCR foi concluído antes
        de executar uma operação que depende
        dos dados extraídos.
        """

        if receipt.ocr_status != Receipt.OCRStatus.COMPLETED:

            raise OCRNotCompletedError()

        return receipt
