from apps.core.exceptions import (
    NotFoundError,
    AlreadyExistsError,
)


class TagNotFoundError(NotFoundError):
    """Tag não encontrada."""


class TagAlreadyExistsError(AlreadyExistsError):
    """Já existe uma tag com esse nome para o usuário."""