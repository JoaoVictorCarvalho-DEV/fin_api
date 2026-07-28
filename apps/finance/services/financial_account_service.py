from django.db import transaction

from apps.finance.models.financial_account import FinancialAccount
from apps.finance.exceptions.financial_account_exceptions import (
    FinancialAccountNotFoundError,
    FinancialAccountAlreadyExistsError,
    FinancialAccountHasTransactionsError,
)


class FinancialAccountService:
    """
    Regras de negócio relacionadas às contas financeiras.
    """

    @staticmethod
    def create(user, data):
        """
        Cria uma nova conta financeira.
        """

        if FinancialAccount.objects.filter(
            user=user,
            name=data["name"]
        ).exists():

            raise FinancialAccountAlreadyExistsError(
                "Já existe uma conta com esse nome."
            )

        with transaction.atomic():

            account = FinancialAccount.objects.create(
                user=user,
                **data
            )

        return account


    @staticmethod
    def get_by_id(user, account_id):
        """
        Busca uma conta pertencente ao usuário.
        """

        try:
            return FinancialAccount.objects.get(
                id=account_id,
                user=user
            )

        except FinancialAccount.DoesNotExist:
            raise FinancialAccountNotFoundError(
                "Conta financeira não encontrada."
            )


    @staticmethod
    def list(user):
        """
        Lista contas do usuário.
        """

        return FinancialAccount.objects.filter(
            user=user
        )


    @staticmethod
    def update(account, data):
        """
        Atualiza uma conta existente.
        """

        for field, value in data.items():
            setattr(
                account,
                field,
                value
            )

        account.full_clean()
        account.save()

        return account


    @staticmethod
    def deactivate(account):
        """
        Desativa uma conta.
        """

        account.is_active = False
        account.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return account


    @staticmethod
    def activate(account):
        """
        Ativa uma conta.
        """

        account.is_active = True
        account.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return account


    @staticmethod
    def delete(account):
        """
        Remove uma conta caso não possua transações.
        """

        if account.transactions.exists():
            raise FinancialAccountHasTransactionsError(
                "Não é possível remover uma conta com transações."
            )

        account.delete()