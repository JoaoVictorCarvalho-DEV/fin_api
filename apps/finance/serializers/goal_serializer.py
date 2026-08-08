from rest_framework import serializers

from apps.finance.models.goal import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            "id",
            "name",
            "target_amount",
            "saved_amount",
            "start_date",
            "target_date",
            "status",
            "category",
            "related_account",
            "description",
            "priority",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class GoalCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = (
            "name",
            "target_amount",
            "saved_amount",
            "start_date",
            "target_date",
            "status",
            "category",
            "related_account",
            "description",
            "priority",
        )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        target_date = attrs.get("target_date")

        if start_date and target_date and target_date <= start_date:
            raise serializers.ValidationError(
                {"target_date": "A data alvo deve ser posterior à data inicial."}
            )

        return attrs
