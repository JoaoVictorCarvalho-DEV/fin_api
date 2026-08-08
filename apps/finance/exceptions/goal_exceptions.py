class GoalNotFoundError(Exception):
    """Exceção lançada quando uma meta não é encontrada."""

    def __init__(self, message="Meta não encontrada."):
        super().__init__(message)


class GoalAlreadyExistsError(Exception):
    """Exceção lançada quando uma meta já existe para o usuário."""

    def __init__(self, message="Já existe uma meta com esse nome."):
        super().__init__(message)
