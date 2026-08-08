class ReceiptNotFoundError(Exception):
    """
    Exceção lançada quando o recibo não é encontrado.
    """

    def __init__(self, receipt_id=None):
        if receipt_id:
            message = f"Recibo com ID {receipt_id} não encontrado."
        else:
            message = "Recibo não encontrado."

        super().__init__(message)


class ReceiptAlreadyExistsError(Exception):
    """
    Exceção lançada quando uma transação já possui um recibo.
    """

    def __init__(self, transaction_id=None):
        if transaction_id:
            message = (
                f"A transação com ID {transaction_id} "
                "já possui um recibo."
            )
        else:
            message = "Esta transação já possui um recibo."

        super().__init__(message)


class ReceiptFileRequiredError(Exception):
    """
    Exceção lançada quando nenhum arquivo é informado.
    """

    def __init__(self):
        super().__init__(
            "É necessário informar um arquivo para o recibo."
        )


class ReceiptFileAlreadyExistsError(Exception):
    """
    Exceção lançada quando o arquivo já foi cadastrado.
    """

    def __init__(self):
        super().__init__(
            "Este arquivo já foi cadastrado."
        )


class OCRProcessingError(Exception):
    """
    Exceção lançada quando ocorre um erro durante o processamento OCR.
    """

    def __init__(self, message=None):
        if message:
            error_message = (
                f"Erro ao processar OCR: {message}"
            )
        else:
            error_message = (
                "Ocorreu um erro durante o processamento OCR."
            )

        super().__init__(error_message)


class OCRAlreadyProcessingError(Exception):
    """
    Exceção lançada quando o OCR já está sendo processado.
    """

    def __init__(self):
        super().__init__(
            "O OCR deste recibo já está sendo processado."
        )


class OCRNotCompletedError(Exception):
    """
    Exceção lançada quando uma operação exige
    que o OCR esteja concluído.
    """

    def __init__(self):
        super().__init__(
            "O processamento OCR ainda não foi concluído."
        )
