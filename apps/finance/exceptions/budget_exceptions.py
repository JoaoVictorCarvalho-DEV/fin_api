from apps.core.exceptions import (
    NotFoundError,
    AlreadyExistsError,
)


class BudgetNotFoundError(NotFoundError):
    """Orçamento não encontrado."""


class BudgetAlreadyExistsError(AlreadyExistsError):
    """Já existe um orçamento para esta categoria no período informado."""