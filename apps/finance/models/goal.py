from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.finance.models.category import Category
from apps.finance.models.financial_account import FinancialAccount

class Goal(models.Model):
    """
    Metas financeiras do usuário
    """
    
    class StatusChoices(models.TextChoices):
        ACTIVE = "ACTIVE", "Ativa"
        ACHIEVED = "ACHIEVED", "Alcançada"
        FAILED = "FAILED", "Falha"
        CANCELED = "CANCELED", "Cancelada"
    
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='goals'
    )
    name = models.CharField('Nome', max_length=100)
    target_amount = models.DecimalField(
        'Valor alvo',
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01"))
        ]
    )   
    saved_amount = models.DecimalField(
        'Valor economizado',
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0.00"))
        ]
    )
    
    start_date = models.DateField('Data Início')
    target_date = models.DateField('Data Alvo')
    status = models.CharField(
        'Status', 
        max_length=20, 
        choices=StatusChoices.choices, 
        default=StatusChoices.ACTIVE
    )
    
    # Opções
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goals'
    )
    related_account = models.ForeignKey(
        FinancialAccount, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='goals'
    )
    
    description = models.TextField('Descrição', blank=True)
    priority = models.PositiveSmallIntegerField(
        'Prioridade', 
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Meta'
        verbose_name_plural = 'Metas'
        ordering = ['-priority', 'target_date']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['target_date']),
            models.Index(fields=['user', 'status']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "name"
                ],
                name="unique_goal_name_per_user"
            )
        ]
    
    def clean(self):
        if self.target_date <= self.start_date:
            raise ValidationError(
                "A data alvo deve ser posterior à data inicial."
            )
    
    def __str__(self):
        return (
            f"{self.name} "
            f"({self.user})"
        )
    