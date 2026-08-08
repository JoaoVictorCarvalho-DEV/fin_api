from django.db import transaction

from apps.finance.models.tag import Tag
from apps.finance.exceptions import (
    TagNotFoundError,
    TagAlreadyExistsError,
)


class TagService:

    @staticmethod
    def list(user):

        return Tag.objects.filter(
            user=user,
            is_active=True,
        ).order_by(
            "name",
        )

    @staticmethod
    def get_by_id(user, tag_id):

        tag = Tag.objects.filter(
            id=tag_id,
            user=user,
            is_active=True,
        ).first()

        if tag is None:
            raise TagNotFoundError(
                "Tag não encontrada."
            )

        return tag

    @staticmethod
    def create(user, data):

        if Tag.objects.filter(
            user=user,
            name=data["name"],
        ).exists():

            raise TagAlreadyExistsError(
                "Já existe uma tag com esse nome."
            )

        with transaction.atomic():

            return Tag.objects.create(
                user=user,
                **data,
            )

    @staticmethod
    def update(tag, data):

        name = data.get(
            "name",
            tag.name
        )

        if Tag.objects.filter(
            user=tag.user,
            name=name,
        ).exclude(
            id=tag.id
        ).exists():

            raise TagAlreadyExistsError(
                "Já existe uma tag com esse nome."
            )

        with transaction.atomic():

            for field, value in data.items():
                setattr(
                    tag,
                    field,
                    value
                )

            tag.save()

        return tag

    @staticmethod
    def deactivate(tag):

        tag.is_active = False

        tag.save(
            update_fields=[
                "is_active"
            ]
        )

        return tag