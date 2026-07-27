from decimal import Decimal

from django.db import models
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from django.core.exceptions import ValidationError

from apps.finance.models.category import Category


class Budget(models.Model):
    """
    Orçamentos definidos pelo usuário para controle financeiro.
    """

    class PeriodChoices(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Mensal'
        YEARLY = 'YEARLY', 'Anual'
        CUSTOM = 'CUSTOM', 'Personalizado'


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='budgets'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='budgets'
    )

    amount = models.DecimalField(
        'Valor',
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01'))
        ]
    )

    period = models.CharField(
        'Período',
        max_length=20,
        choices=PeriodChoices,
        default=PeriodChoices.MONTHLY
    )

    start_date = models.DateField(
        'Data inicial'
    )

    end_date = models.DateField(
        'Data final'
    )

    alert_threshold = models.DecimalField(
        'Limite de alerta (%)',
        max_digits=5,
        decimal_places=2,
        default=80,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )


    class Meta:
        verbose_name = 'Orçamento'
        verbose_name_plural = 'Orçamentos'

        ordering = [
            '-created_at'
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    'user',
                    'category',
                    'start_date',
                    'end_date'
                ],
                name='unique_budget_period'
            )
        ]


    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                'A data inicial não pode ser maior que a data final.'
            )


    def __str__(self):
        return (
            f'{self.category.name} - '
            f'R$ {self.amount}'
        )