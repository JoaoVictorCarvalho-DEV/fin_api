from django.db import transaction

from apps.finance.models.budget import Budget
from apps.finance.exceptions import (
    BudgetNotFoundError,
    BudgetAlreadyExistsError,
)


class BudgetService:

    @staticmethod
    def list(user):

        return Budget.objects.filter(
            user=user,
        ).select_related(
            "category"
        ).order_by(
            "-created_at",
        )

    @staticmethod
    def get_by_id(user, budget_id):

        budget = Budget.objects.select_related(
            "category"
        ).filter(
            id=budget_id,
            user=user,
        ).first()

        if budget is None:
            raise BudgetNotFoundError(
                "Orçamento não encontrado."
            )

        return budget

    @staticmethod
    def create(user, data):

        if Budget.objects.filter(
            user=user,
            category=data["category"],
            start_date=data["start_date"],
            end_date=data["end_date"],
        ).exists():

            raise BudgetAlreadyExistsError(
                "Já existe um orçamento para esta categoria no período informado."
            )

        with transaction.atomic():

            return Budget.objects.create(
                user=user,
                **data,
            )

    @staticmethod
    def update(budget, data):

        category = data.get(
            "category",
            budget.category
        )

        start_date = data.get(
            "start_date",
            budget.start_date
        )

        end_date = data.get(
            "end_date",
            budget.end_date
        )

        if Budget.objects.filter(
            user=budget.user,
            category=category,
            start_date=start_date,
            end_date=end_date,
        ).exclude(
            id=budget.id
        ).exists():

            raise BudgetAlreadyExistsError(
                "Já existe um orçamento para esta categoria no período informado."
            )

        with transaction.atomic():

            for field, value in data.items():
                setattr(
                    budget,
                    field,
                    value
                )

            budget.save()

        return budget

    @staticmethod
    def delete(budget):

        with transaction.atomic():

            budget.delete()