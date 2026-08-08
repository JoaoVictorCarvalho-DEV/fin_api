class RecurringTransactionNotFoundError(Exception):
    """Exceção lançada quando uma transação recorrente não é encontrada."""

    def __init__(self, message="Transação recorrente não encontrada."):
        super().__init__(message)


class RecurringTransactionAlreadyExistsError(Exception):
    """Exceção lançada quando uma transação recorrente já existe para o usuário."""

    def __init__(self, message="Já existe uma transação recorrente com essa descrição."):
        super().__init__(message)
