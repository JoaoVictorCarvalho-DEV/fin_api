class CategoryError(Exception):
    """Exceção base para categoria."""


class CategoryNotFoundError(CategoryError):
    """Categoria não encontrada."""


class CategoryAlreadyExistsError(CategoryError):
    """Já existe uma categoria com esse nome para o usuário."""