
from rest_framework import serializers

from apps.finance.models.transaction import Transaction
from apps.finance.models.category import Category
from apps.finance.models.financial_account import FinancialAccount
from apps.finance.models.tag import Tag


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer para leitura de transações.
    """

    type_display = serializers.CharField(
        source="get_type_display",
        read_only=True,
    )

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    is_income = serializers.BooleanField(
        read_only=True,
    )

    is_expense = serializers.BooleanField(
        read_only=True,
    )

    is_transfer = serializers.BooleanField(
        read_only=True,
    )

    is_completed = serializers.BooleanField(
        read_only=True,
    )

    is_pending = serializers.BooleanField(
        read_only=True,
    )

    is_canceled = serializers.BooleanField(
        read_only=True,
    )

    is_installment = serializers.BooleanField(
        read_only=True,
    )

    installment_info = serializers.CharField(
        read_only=True,
    )

    class Meta:
        model = Transaction

        fields = (
            "id",
            "account",
            "category",
            "tags",
            "description",
            "amount",
            "type",
            "type_display",
            "date",
            "status",
            "status_display",
            "notes",
            "related_transaction",
            "bank_statement_id",
            "reconciled_at",
            "installment_number",
            "total_installments",
            "parent_transaction",
            "is_income",
            "is_expense",
            "is_transfer",
            "is_completed",
            "is_pending",
            "is_canceled",
            "is_installment",
            "installment_info",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "type_display",
            "status_display",
            "is_income",
            "is_expense",
            "is_transfer",
            "is_completed",
            "is_pending",
            "is_canceled",
            "is_installment",
            "installment_info",
            "created_at",
            "updated_at",
        )


class TransactionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de transações.
    """

    class Meta:
        model = Transaction

        fields = (
            "account",
            "category",
            "tags",
            "description",
            "amount",
            "type",
            "date",
            "notes",
            "related_transaction",
            "bank_statement_id",
            "installment_number",
            "total_installments",
            "parent_transaction",
        )

    def validate_account(self, account):
        """
        Garante que a conta pertence ao usuário autenticado.
        """

        user = self.context["request"].user

        if account.user_id != user.id:
            raise serializers.ValidationError(
                "A conta financeira não pertence ao usuário."
            )

        return account

    def validate_category(self, category):
        """
        Garante que a categoria é válida.
        """

        if category is None:
            return category

        return category

    def validate_tags(self, tags):
        """
        Garante que todas as tags pertencem ao usuário.
        """

        user = self.context["request"].user

        invalid_tags = [
            tag
            for tag in tags
            if tag.user_id != user.id
        ]

        if invalid_tags:
            raise serializers.ValidationError(
                "Uma ou mais tags não pertencem ao usuário."
            )

        return tags

    def validate_related_transaction(
        self,
        related_transaction,
    ):
        """
        Valida a transação relacionada.
        """

        if related_transaction is None:
            return related_transaction

        user = self.context["request"].user

        if related_transaction.user_id != user.id:
            raise serializers.ValidationError(
                "A transação relacionada não pertence ao usuário."
            )

        return related_transaction

    def validate_parent_transaction(
        self,
        parent_transaction,
    ):
        """
        Valida a transação pai.
        """

        if parent_transaction is None:
            return parent_transaction

        user = self.context["request"].user

        if parent_transaction.user_id != user.id:
            raise serializers.ValidationError(
                "A transação pai não pertence ao usuário."
            )

        return parent_transaction

    def validate(self, attrs):
        """
        Valida regras relacionadas aos campos da transação.
        """

        transaction_type = attrs.get("type")
        related_transaction = attrs.get(
            "related_transaction"
        )

        installment_number = attrs.get(
            "installment_number"
        )

        total_installments = attrs.get(
            "total_installments"
        )

        # Transferências precisam de uma transação relacionada.
        if (
            transaction_type
            == Transaction.TransactionType.TRANSFER
            and related_transaction is None
        ):
            raise serializers.ValidationError(
                {
                    "related_transaction": (
                        "Transferências devem possuir "
                        "uma transação relacionada."
                    )
                }
            )

        # Apenas transferências deveriam utilizar
        # related_transaction.
        if (
            transaction_type
            != Transaction.TransactionType.TRANSFER
            and related_transaction is not None
        ):
            raise serializers.ValidationError(
                {
                    "related_transaction": (
                        "A transação relacionada só pode "
                        "ser utilizada em transferências."
                    )
                }
            )

        # Número da parcela e total precisam ser informados juntos.
        if (
            installment_number is not None
            and total_installments is None
        ):
            raise serializers.ValidationError(
                {
                    "total_installments": (
                        "Informe o total de parcelas."
                    )
                }
            )

        if (
            total_installments is not None
            and installment_number is None
        ):
            raise serializers.ValidationError(
                {
                    "installment_number": (
                        "Informe o número da parcela."
                    )
                }
            )

        if (
            installment_number is not None
            and total_installments is not None
            and installment_number > total_installments
        ):
            raise serializers.ValidationError(
                {
                    "installment_number": (
                        "Número da parcela não pode "
                        "ser maior que o total."
                    )
                }
            )

        return attrs


class TransactionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualização de transações.
    """

    class Meta:
        model = Transaction

        fields = (
            "account",
            "category",
            "tags",
            "description",
            "amount",
            "type",
            "date",
            "status",
            "notes",
            "related_transaction",
            "bank_statement_id",
            "installment_number",
            "total_installments",
            "parent_transaction",
        )

    def validate_account(self, account):
        """
        Garante que a conta pertence ao usuário.
        """

        user = self.context["request"].user

        if account.user_id != user.id:
            raise serializers.ValidationError(
                "A conta financeira não pertence ao usuário."
            )

        return account

    def validate_tags(self, tags):
        """
        Garante que todas as tags pertencem ao usuário.
        """

        user = self.context["request"].user

        invalid_tags = [
            tag
            for tag in tags
            if tag.user_id != user.id
        ]

        if invalid_tags:
            raise serializers.ValidationError(
                "Uma ou mais tags não pertencem ao usuário."
            )

        return tags

    def validate_related_transaction(
        self,
        related_transaction,
    ):
        """
        Garante que a transação relacionada
        pertence ao usuário.
        """

        if related_transaction is None:
            return related_transaction

        user = self.context["request"].user

        if related_transaction.user_id != user.id:
            raise serializers.ValidationError(
                "A transação relacionada não pertence ao usuário."
            )

        return related_transaction

    def validate_parent_transaction(
        self,
        parent_transaction,
    ):
        """
        Garante que a transação pai pertence ao usuário.
        """

        if parent_transaction is None:
            return parent_transaction

        user = self.context["request"].user

        if parent_transaction.user_id != user.id:
            raise serializers.ValidationError(
                "A transação pai não pertence ao usuário."
            )

        return parent_transaction

    def validate(self, attrs):
        """
        Valida regras relacionadas aos campos da transação.
        """

        transaction_type = attrs.get("type")

        # Em PATCH, se type não foi enviado,
        # utiliza o valor atual da transação.
        if transaction_type is None:
            transaction_type = self.instance.type

        related_transaction = attrs.get(
            "related_transaction",
            self.instance.related_transaction,
        )

        installment_number = attrs.get(
            "installment_number",
            self.instance.installment_number,
        )

        total_installments = attrs.get(
            "total_installments",
            self.instance.total_installments,
        )

        if (
            transaction_type
            == Transaction.TransactionType.TRANSFER
            and related_transaction is None
        ):
            raise serializers.ValidationError(
                {
                    "related_transaction": (
                        "Transferências devem possuir "
                        "uma transação relacionada."
                    )
                }
            )

        if (
            transaction_type
            != Transaction.TransactionType.TRANSFER
            and related_transaction is not None
        ):
            raise serializers.ValidationError(
                {
                    "related_transaction": (
                        "A transação relacionada só pode "
                        "ser utilizada em transferências."
                    )
                }
            )

        if (
            installment_number is not None
            and total_installments is None
        ):
            raise serializers.ValidationError(
                {
                    "total_installments": (
                        "Informe o total de parcelas."
                    )
                }
            )

        if (
            total_installments is not None
            and installment_number is None
        ):
            raise serializers.ValidationError(
                {
                    "installment_number": (
                        "Informe o número da parcela."
                    )
                }
            )

        if (
            installment_number is not None
            and total_installments is not None
            and installment_number > total_installments
        ):
            raise serializers.ValidationError(
                {
                    "installment_number": (
                        "Número da parcela não pode "
                        "ser maior que o total."
                    )
                }
            )

        return attrs

