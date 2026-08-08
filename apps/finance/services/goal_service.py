from django.db import transaction

from apps.finance.models.goal import Goal
from apps.finance.exceptions import GoalNotFoundError, GoalAlreadyExistsError


class GoalService:
    @staticmethod
    def list(user):
        return Goal.objects.filter(user=user).select_related("category", "related_account").order_by("-priority", "target_date")

    @staticmethod
    def get_by_id(user, goal_id):
        goal = (
            Goal.objects.filter(id=goal_id, user=user)
            .select_related("category", "related_account")
            .first()
        )

        if goal is None:
            raise GoalNotFoundError("Meta não encontrada.")

        return goal

    @staticmethod
    def create(user, data):
        if Goal.objects.filter(user=user, name=data["name"]).exists():
            raise GoalAlreadyExistsError("Já existe uma meta com esse nome.")

        with transaction.atomic():
            return Goal.objects.create(user=user, **data)

    @staticmethod
    def update(goal, data):
        name = data.get("name", goal.name)
        if Goal.objects.filter(user=goal.user, name=name).exclude(id=goal.id).exists():
            raise GoalAlreadyExistsError("Já existe uma meta com esse nome.")

        with transaction.atomic():
            for field, value in data.items():
                setattr(goal, field, value)

            goal.full_clean()
            goal.save()

        return goal

    @staticmethod
    def delete(goal):
        goal.delete()
        return True
