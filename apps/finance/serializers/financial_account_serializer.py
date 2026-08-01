from rest_framework import serializers

from apps.finance.models.financial_account import FinancialAccount

from rest_framework import serializers

from apps.finance.models.financial_account import FinancialAccount


class FinancialAccountSerializer(serializers.ModelSerializer):

    account_type_display = serializers.CharField(
        source="get_account_type_display",
        read_only=True
    )

    class Meta:
        model = FinancialAccount

        fields = (
            "id",
            "name",
            "account_type",
            "account_type_display",
            "initial_balance",
            "description",
            "institution",
            "account_number",
            "agency_number",
            "credit_limit",
            "closing_day",
            "due_day",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )        

class FinancialAccountCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = FinancialAccount

        exclude = (
            "user",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):

        account_type = attrs.get(
            "account_type",
            getattr(self.instance, "account_type", None)
        )

        credit_limit = attrs.get(
            "credit_limit",
            getattr(self.instance, "credit_limit", None)
        )

        closing_day = attrs.get(
            "closing_day",
            getattr(self.instance, "closing_day", None)
        )

        due_day = attrs.get(
            "due_day",
            getattr(self.instance, "due_day", None)
        )

        if account_type == FinancialAccount.AccountType.CREDIT_CARD:

            if credit_limit is None:
                raise serializers.ValidationError(
                    {
                        "credit_limit": (
                            "Informe o limite do cartão."
                        )
                    }
                )

            if closing_day is None:
                raise serializers.ValidationError(
                    {
                        "closing_day": (
                            "Informe o dia de fechamento."
                        )
                    }
                )

            if due_day is None:
                raise serializers.ValidationError(
                    {
                        "due_day": (
                            "Informe o dia de vencimento."
                        )
                    }
                )

        return attrs