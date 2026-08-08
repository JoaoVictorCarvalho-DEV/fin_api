class TransactionNotFoundError(Exception):
    """
    Exceção lançada quando uma transação não é encontrada.
    """

    def __init__(self, message="Transação não encontrada."):
        super().__init__(message)


class TransactionAlreadyExistsError(Exception):
    """
    Exceção lançada quando uma transação já existe
    e não deveria ser duplicada.
    """

    def __init__(
        self,
        message="A transação já existe.",
    ):
        super().__init__(message)


class TransactionAccountNotFoundError(Exception):
    """
    Exceção lançada quando a conta financeira
    associada à transação não é encontrada.
    """

    def __init__(
        self,
        message="Conta financeira não encontrada.",
    ):
        super().__init__(message)


class TransactionCategoryNotFoundError(Exception):
    """
    Exceção lançada quando a categoria
    associada à transação não é encontrada.
    """

    def __init__(
        self,
        message="Categoria não encontrada.",
    ):
        super().__init__(message)


class TransactionTagNotFoundError(Exception):
    """
    Exceção lançada quando uma ou mais tags
    associadas à transação não são encontradas.
    """

    def __init__(
        self,
        message="Uma ou mais tags não foram encontradas.",
    ):
        super().__init__(message)


class TransactionRelatedNotFoundError(Exception):
    """
    Exceção lançada quando a transação relacionada
    não é encontrada.
    """

    def __init__(
        self,
        message="Transação relacionada não encontrada.",
    ):
        super().__init__(message)


class TransactionParentNotFoundError(Exception):
    """
    Exceção lançada quando a transação pai
    não é encontrada.
    """

    def __init__(
        self,
        message="Transação pai não encontrada.",
    ):
        super().__init__(message)


class TransactionInvalidTypeError(Exception):
    """
    Exceção lançada quando o tipo da transação
    não é compatível com a operação realizada.
    """

    def __init__(
        self,
        message="Tipo de transação inválido.",
    ):
        super().__init__(message)


class TransactionTransferError(Exception):
    """
    Exceção relacionada às regras de transferência.
    """

    def __init__(
        self,
        message=(
            "Não foi possível realizar "
            "a transferência."
        ),
    ):
        super().__init__(message)


class TransactionRelatedToItselfError(Exception):
    """
    Exceção lançada quando uma transação
    tenta apontar para ela mesma.
    """

    def __init__(
        self,
        message=(
            "Uma transação não pode "
            "apontar para ela mesma."
        ),
    ):
        super().__init__(message)


class TransactionInstallmentError(Exception):
    """
    Exceção relacionada às regras de parcelamento.
    """

    def __init__(
        self,
        message="Dados de parcelamento inválidos.",
    ):
        super().__init__(message)


class TransactionInvalidInstallmentError(Exception):
    """
    Exceção lançada quando o número da parcela
    é maior que o total de parcelas.
    """

    def __init__(
        self,
        message=(
            "O número da parcela não pode "
            "ser maior que o total de parcelas."
        ),
    ):
        super().__init__(message)


class TransactionCannotDeleteError(Exception):
    """
    Exceção lançada quando uma transação
    não pode ser excluída.
    """

    def __init__(
        self,
        message="A transação não pode ser excluída.",
    ):
        super().__init__(message)


class TransactionCannotUpdateError(Exception):
    """
    Exceção lançada quando uma transação
    não pode ser atualizada.
    """

    def __init__(
        self,
        message="A transação não pode ser atualizada.",
    ):
        super().__init__(message)
