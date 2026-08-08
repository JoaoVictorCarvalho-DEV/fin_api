class ApplicationError(Exception):
    """
    Exceção base da aplicação.
    """
    
    default_message = "Erro interno da aplicação."

    def __init__(self, message=None):
        self.message = message or self.default_message

        super().__init__(self.message)


class NotFoundError(ApplicationError):
    """
    Recurso não encontrado.
    """

    status_code = 404


class AlreadyExistsError(ApplicationError):
    """
    Recurso já existente.
    """

    status_code = 409