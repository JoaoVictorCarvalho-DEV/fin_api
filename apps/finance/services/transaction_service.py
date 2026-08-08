from django.db import transaction

from apps.finance.models.transaction import Transaction
from apps.finance.exceptions import (
    TransactionNotFoundError,
    TransactionAlreadyExistsError,
)


class TransactionService:
    """
    Regras de negócio relacionadas às transações financeiras.
    """

    @staticmethod
    def list(user):
        return (
            Transaction.objects.filter(user=user)
            .select_related("account", "category", "user")
            .prefetch_related("tags")
            .order_by("-date", "-created_at")
        )

    @staticmethod
    def get_by_id(user, transaction_id):
        transaction_obj = (
            Transaction.objects.filter(id=transaction_id, user=user)
            .select_related("account", "category", "user")
            .prefetch_related("tags")
            .first()
        )

        if transaction_obj is None:
            raise TransactionNotFoundError("Transação não encontrada.")

        return transaction_obj

    @staticmethod
    def create(user, data):
        data = dict(data)
        tags = data.pop("tags", None)

        with transaction.atomic():
            transaction_obj = Transaction.objects.create(
                user=user,
                **data,
            )

            if tags is not None:
                transaction_obj.tags.set(tags)

        return transaction_obj

    @staticmethod
    def update(transaction_obj, data):
        with transaction.atomic():
            tags = data.pop("tags", None)

            for field, value in data.items():
                setattr(transaction_obj, field, value)

            transaction_obj.save()

            if tags is not None:
                transaction_obj.tags.set(tags)

        return transaction_obj

    @staticmethod
    def delete(transaction_obj):
        transaction_obj.delete()
        return True
