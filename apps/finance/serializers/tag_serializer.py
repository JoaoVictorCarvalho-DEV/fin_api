from rest_framework import serializers

from apps.finance.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag

        fields = (
            "id",
            "name",
            "color",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "O nome deve possuir pelo menos 2 caracteres."
            )

        return value