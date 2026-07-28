class FinancialAccountError(Exception):
    """Exceção base para contas financeiras."""
    pass


class FinancialAccountNotFoundError(FinancialAccountError):
    """Conta financeira não encontrada."""
    pass


class FinancialAccountAlreadyExistsError(FinancialAccountError):
    """Já existe uma conta financeira com esse nome para o usuário."""
    pass


class FinancialAccountInactiveError(FinancialAccountError):
    """A conta financeira está inativa."""
    pass


class FinancialAccountHasTransactionsError(FinancialAccountError):
    """A conta financeira possui transações vinculadas."""
    pass