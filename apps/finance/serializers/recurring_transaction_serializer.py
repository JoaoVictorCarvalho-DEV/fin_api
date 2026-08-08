from rest_framework import serializers

from apps.finance.models.recurring_transaction import RecurringTransaction


class RecurringTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = (
            "id",
            "account",
            "category",
            "description",
            "amount",
            "transaction_type",
            "notes",
            "frequency",
            "start_date",
            "end_date",
            "next_execution",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class RecurringTransactionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringTransaction
        fields = (
            "account",
            "category",
            "description",
            "amount",
            "transaction_type",
            "notes",
            "frequency",
            "start_date",
            "end_date",
            "next_execution",
            "is_active",
        )

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        next_execution = attrs.get("next_execution")

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError(
                {"end_date": "A data final deve ser posterior à data inicial."}
            )

        if next_execution and start_date and next_execution < start_date:
            raise serializers.ValidationError(
                {"next_execution": "A próxima execução não pode ser anterior à data inicial."}
            )

        return attrs
