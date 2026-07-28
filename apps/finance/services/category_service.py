from django.db import transaction

from apps.finance.models.category import Category
from apps.finance.exceptions import (
    CategoryNotFoundError,
    CategoryAlreadyExistsError,
)


class CategoryService:


    @staticmethod
    def list(user):

        return Category.objects.filter(
            user=user,
            is_active=True,
        ).order_by(
            "type",
            "name",
        )


    @staticmethod
    def get_by_id(user, category_id):

        category = Category.objects.filter(
            id=category_id,
            user=user,
            is_active=True,
        ).first()

        if category is None:
            raise CategoryNotFoundError(
                "Categoria não encontrada."
            )

        return category


    @staticmethod
    def create(user, data):

        if Category.objects.filter(
            user=user,
            name=data["name"],
            type=data["type"],
        ).exists():

            raise CategoryAlreadyExistsError(
                "Já existe uma categoria com esse nome."
            )


        with transaction.atomic():

            return Category.objects.create(
                user=user,
                **data,
            )


    @staticmethod
    def update(category, data):

        name = data.get(
            "name",
            category.name
        )

        category_type = data.get(
            "type",
            category.type
        )


        if Category.objects.filter(
            user=category.user,
            name=name,
            type=category_type,
        ).exclude(
            id=category.id
        ).exists():

            raise CategoryAlreadyExistsError(
                "Já existe uma categoria com esse nome."
            )


        with transaction.atomic():

            for field, value in data.items():
                setattr(
                    category,
                    field,
                    value
                )

            category.save()


        return category


    @staticmethod
    def deactivate(category):

        category.is_active = False

        category.save(
            update_fields=[
                "is_active"
            ]
        )

        return category