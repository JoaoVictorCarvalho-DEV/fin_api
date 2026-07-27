class CategoryNotFoundError(Exception):
    """Categoria não encontrada."""
    pass


class CategoryAlreadyExistsError(Exception):
    """Já existe uma categoria com esse nome para o usuário."""
    pass