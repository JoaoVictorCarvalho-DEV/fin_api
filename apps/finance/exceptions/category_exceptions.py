from apps.core.exceptions import (
    NotFoundError,
    AlreadyExistsError,
)

class CategoryNotFoundError(NotFoundError):
    """Categoria não encontrada."""


class CategoryAlreadyExistsError(AlreadyExistsError):
    """Já existe uma categoria com esse nome para o usuário."""