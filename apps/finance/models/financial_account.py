from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from jsonschema import ValidationError

class FinancialAccount(models.Model):
    """
    Contas financeiras do usuário
    Representa onde está o dinheiro
    """
    
    class AccountType(models.TextChoices):
        BANK = "BANK", "Banco"
        CASH = "CASH", "Dinheiro"
        CREDIT_CARD = "CREDIT_CARD", "Cartão de Crédito"
        INVESTMENT = "INVESTMENT", "Investimento"
        OTHER = "OTHER", "Outro"
        
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    name = models.CharField('Nome', max_length=100)
    account_type = models.CharField(
        'Tipo', 
        max_length=20, 
        choices=AccountType.choices
    )
    initial_balance = models.DecimalField(
        'Saldo Inicial',
        max_digits=12, 
        decimal_places=2, 
        default=0.00
    )
    description = models.TextField('Descrição', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    
    # Campos adicionais
    institution = models.CharField('Instituição', max_length=100, blank=True)
    account_number = models.CharField('Número da Conta', max_length=50, blank=True)
    agency_number = models.CharField('Agência', max_length=20, blank=True)
    credit_limit = models.DecimalField(
        'Limite de Crédito',
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Para contas de crédito"
    )
    closing_day = models.PositiveSmallIntegerField(
        'Dia de Fechamento',
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text="Dia de fechamento da fatura (cartão de crédito)"
    )
    due_day = models.PositiveSmallIntegerField(
        'Dia de Vencimento',
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        help_text="Dia de vencimento (cartão de crédito)"
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        db_table = 'finance_financial_account'
        verbose_name = 'Conta Financeira'
        verbose_name_plural = 'Contas Financeiras'
        ordering = ['name']
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["account_type"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["user", "is_active"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "name"
                ],
                name="unique_account_name_per_user"
            )
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_account_type_display()}"
    
    def clean(self):
        if (
            self.account_type != self.AccountType.CREDIT_CARD
            and any([
                self.credit_limit is not None,
                self.closing_day is not None,
                self.due_day is not None,
            ])
        ):
            raise ValidationError(
                "Limite, fechamento e vencimento só podem ser usados em cartão de crédito."
            )
    
