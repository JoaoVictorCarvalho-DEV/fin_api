from django.db import transaction

from apps.finance.models.recurring_transaction import RecurringTransaction
from apps.finance.exceptions import (
    RecurringTransactionAlreadyExistsError,
    RecurringTransactionNotFoundError,
)


class RecurringTransactionService:
    @staticmethod
    def list(user):
        return (
            RecurringTransaction.objects.filter(user=user)
            .select_related("account", "category")
            .order_by("next_execution", "-created_at")
        )

    @staticmethod
    def get_by_id(user, recurring_transaction_id):
        recurring_transaction = (
            RecurringTransaction.objects.filter(id=recurring_transaction_id, user=user)
            .select_related("account", "category")
            .first()
        )

        if recurring_transaction is None:
            raise RecurringTransactionNotFoundError("Transação recorrente não encontrada.")

        return recurring_transaction

    @staticmethod
    def create(user, data):
        if RecurringTransaction.objects.filter(
            user=user,
            description=data["description"],
            account=data["account"],
            frequency=data["frequency"],
        ).exists():
            raise RecurringTransactionAlreadyExistsError(
                "Já existe uma transação recorrente com essa descrição."
            )

        with transaction.atomic():
            return RecurringTransaction.objects.create(user=user, **data)

    @staticmethod
    def update(recurring_transaction, data):
        description = data.get("description", recurring_transaction.description)
        account = data.get("account", recurring_transaction.account)
        frequency = data.get("frequency", recurring_transaction.frequency)

        if RecurringTransaction.objects.filter(
            user=recurring_transaction.user,
            description=description,
            account=account,
            frequency=frequency,
        ).exclude(id=recurring_transaction.id).exists():
            raise RecurringTransactionAlreadyExistsError(
                "Já existe uma transação recorrente com essa descrição."
            )

        with transaction.atomic():
            for field, value in data.items():
                setattr(recurring_transaction, field, value)

            recurring_transaction.full_clean()
            recurring_transaction.save()

        return recurring_transaction

    @staticmethod
    def delete(recurring_transaction):
        recurring_transaction.delete()
        return True
