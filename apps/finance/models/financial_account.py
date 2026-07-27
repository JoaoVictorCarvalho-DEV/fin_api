from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class FinancialAccount(models.Model):
    """
    Contas financeiras do usuário
    Representa onde está o dinheiro
    """
    
    ACCOUNT_TYPES = [
        ('BANK', 'Banco'),
        ('CASH', 'Dinheiro'),
        ('CREDIT_CARD', 'Cartão de Crédito'),
        ('INVESTMENT', 'Investimento'),
        ('OTHER', 'Outro'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    name = models.CharField('Nome', max_length=100)
    type = models.CharField(
        'Tipo', 
        max_length=20, 
        choices=ACCOUNT_TYPES
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
            models.Index(fields=['user']),
            models.Index(fields=['type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"
    
    @property
    def current_balance(self):
        """Calcula o saldo atual baseado nas transações"""
        from django.db.models import Sum, Case, When, F, DecimalField, Q
        
        transactions = self.transactions.filter(status='COMPLETED')
        
        # Agregação para calcular saldo
        balance = transactions.aggregate(
            total=Sum(
                Case(
                    When(type='INCOME', then='amount'),
                    When(type='EXPENSE', then=-F('amount')),
                    When(
                        type='TRANSFER',
                        then=Case(
                            When(account_id=self.id, then=-F('amount')),
                            default='amount',
                            output_field=DecimalField()
                        )
                    ),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )['total'] or Decimal('0.00')
        
        return self.initial_balance + balance
    
    @property
    def is_credit_card(self):
        """Verifica se é cartão de crédito"""
        return self.type == 'CREDIT_CARD'
    
    def get_balance_on_date(self, date):
        """Retorna o saldo em uma data específica"""
        from django.db.models import Sum, Case, When, F, DecimalField, Q
        
        transactions = self.transactions.filter(
            status='COMPLETED',
            date__lte=date
        )
        
        balance = transactions.aggregate(
            total=Sum(
                Case(
                    When(type='INCOME', then='amount'),
                    When(type='EXPENSE', then=-F('amount')),
                    When(
                        type='TRANSFER',
                        then=Case(
                            When(account_id=self.id, then=-F('amount')),
                            default='amount',
                            output_field=DecimalField()
                        )
                    ),
                    default=0,
                    output_field=DecimalField()
                )
            )
        )['total'] or Decimal('0.00')
        
        return self.initial_balance + balance
