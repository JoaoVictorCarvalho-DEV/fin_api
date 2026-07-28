from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


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

    transaction_template = models.JSONField(
        "Template da transação"
    )

    frequency = models.CharField(
        "Frequência",
        max_length=20,
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.MONTHLY,
    )

    start_date = models.DateField(
        "Data inicial"
    )

    end_date = models.DateField(
        "Data final",
        null=True,
        blank=True,
    )

    next_execution = models.DateField(
        "Próxima execução"
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
        db_table = 'finance_recurring_transaction'
        verbose_name = "Transação recorrente"
        verbose_name_plural = "Transações recorrentes"

        ordering = [
            "next_execution",
        ]

        indexes = [
            models.Index(
                fields=[
                    "next_execution",
                ]
            ),
            models.Index(
                fields=[
                    "is_active",
                ]
            ),
            models.Index(
                fields=[
                    "user",
                    "is_active",
                ]
            ),
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
            f"{self.get_frequency_display()} - "
            f"{self.user}"
        )