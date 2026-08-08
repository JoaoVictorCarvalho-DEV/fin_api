from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from apps.finance.models.category import Category
from apps.finance.models.financial_account import FinancialAccount
from apps.finance.models.transaction import Transaction


class RecurringTransaction(models.Model):
    """
    Configuração de transações recorrentes.
    """

    class FrequencyChoices(models.TextChoices):
        DAILY = "DAILY", "Diário"
        WEEKLY = "WEEKLY", "Semanal"
        BIWEEKLY = "BIWEEKLY", "Quinzenal"
        MONTHLY = "MONTHLY", "Mensal"
        YEARLY = "YEARLY", "Anual"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recurring_transactions",
    )

    account = models.ForeignKey(
        FinancialAccount,
        on_delete=models.PROTECT,
        related_name="recurring_transactions",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="recurring_transactions",
    )

    description = models.CharField(
        "Descrição",
        max_length=255,
    )

    amount = models.DecimalField(
        "Valor",
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01"))
        ],
    )

    transaction_type = models.CharField(
        "Tipo",
        max_length=20,
        choices=Transaction.TransactionType.choices,
    )

    notes = models.TextField(
        "Observações",
        blank=True,
    )

    frequency = models.CharField(
        "Frequência",
        max_length=20,
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.MONTHLY,
    )

    start_date = models.DateField(
        "Data inicial",
    )

    end_date = models.DateField(
        "Data final",
        null=True,
        blank=True,
    )

    next_execution = models.DateField(
        "Próxima execução",
    )

    is_active = models.BooleanField(
        "Ativa",
        default=True,
    )

    created_at = models.DateTimeField(
        "Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        "Atualizado em",
        auto_now=True,
    )

    class Meta:
        verbose_name = "Transação recorrente"
        verbose_name_plural = "Transações recorrentes"

        ordering = [
            "next_execution",
        ]

        indexes = [
            models.Index(fields=["next_execution"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["user", "is_active"]),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "description",
                    "account",
                    "frequency",
                ],
                name="unique_recurring_transaction",
            )
        ]

    def clean(self):
        if (
            self.end_date is not None
            and self.end_date <= self.start_date
        ):
            raise ValidationError(
                "A data final deve ser posterior à data inicial."
            )

    def __str__(self):
        return (
            f"{self.description} "
            f"({self.get_frequency_display()})"
        )