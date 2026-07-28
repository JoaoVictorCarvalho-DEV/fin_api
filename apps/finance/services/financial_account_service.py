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
    def create(user, validated_data):
        """
        Cria uma nova conta financeira.
        """

        if FinancialAccount.objects.filter(
            user=user,
            name=validated_data["name"],
            is_active=True,
        ).exists():

            raise FinancialAccountAlreadyExistsError(
                "Já existe uma conta com esse nome."
            )


        with transaction.atomic():

            account = FinancialAccount.objects.create(
                user=user,
                **validated_data
            )

        return account



    @staticmethod
    def get_by_id(user, account_id):
        """
        Busca uma conta ativa pertencente ao usuário.
        """

        try:

            return FinancialAccount.objects.get(
                id=account_id,
                user=user,
                is_active=True,
            )

        except FinancialAccount.DoesNotExist:

            raise FinancialAccountNotFoundError(
                "Conta financeira não encontrada."
            )



    @staticmethod
    def list(user):
        """
        Lista contas ativas do usuário.
        """

        return FinancialAccount.objects.filter(
            user=user,
            is_active=True,
        )



    @staticmethod
    def update(account, validated_data):
        """
        Atualiza uma conta existente.
        """

        if "name" in validated_data:

            exists = FinancialAccount.objects.filter(
                user=account.user,
                name=validated_data["name"],
                is_active=True,
            ).exclude(
                id=account.id
            ).exists()


            if exists:

                raise FinancialAccountAlreadyExistsError(
                    "Já existe uma conta com esse nome."
                )


        for field, value in validated_data.items():

            setattr(
                account,
                field,
                value
            )


        account.full_clean()

        account.save()

        return account



    @staticmethod
    def delete(account):
        """
        Realiza soft delete da conta.
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
    def restore(account):
        """
        Restaura uma conta desativada.
        """

        account.is_active = True

        account.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return account