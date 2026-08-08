from rest_framework import serializers

from apps.finance.models.budget import Budget


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget

        fields = (
            "id",
            "category",
            "amount",
            "period",
            "start_date",
            "end_date",
            "alert_threshold",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")

        if (
            start_date is not None
            and end_date is not None
            and start_date > end_date
        ):
            raise serializers.ValidationError(
                {
                    "end_date": (
                        "A data final deve ser maior ou igual à data inicial."
                    )
                }
            )

        return attrs