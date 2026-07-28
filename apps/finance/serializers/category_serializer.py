from rest_framework import serializers

from apps.finance.models.category import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category

        fields = (
            "id",
            "name",
            "type",
            "color",
            "icon",
            "description",
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