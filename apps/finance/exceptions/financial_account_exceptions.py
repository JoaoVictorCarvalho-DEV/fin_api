from apps.core.exceptions import (
    ApplicationError,
    NotFoundError,
    AlreadyExistsError,
)

class FinancialAccountNotFoundError(NotFoundError):
    """Conta financeira não encontrada."""
    pass


class FinancialAccountAlreadyExistsError(AlreadyExistsError):
    """Já existe uma conta financeira com esse nome para o usuário."""
    pass


class FinancialAccountInactiveError(ApplicationError):
    """A conta financeira está inativa."""
    pass


class FinancialAccountHasTransactionsError(ApplicationError):
    """A conta financeira possui transações vinculadas."""
    pass