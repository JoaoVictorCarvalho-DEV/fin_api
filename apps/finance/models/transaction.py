from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from apps.finance.models.category import Category
from apps.finance.models.financial_account import FinancialAccount
from apps.finance.models.tag import Tag
from django.core.exceptions import ValidationError

class Transaction(models.Model):
    """
    Registro de todas as movimentações financeiras
    """
    
    class TransactionType(models.TextChoices):
        INCOME = "INCOME", "Receita"
        EXPENSE = "EXPENSE", "Despesa"
        TRANSFER = "TRANSFER", "Transferência"


    class TransactionStatus(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        COMPLETED = "COMPLETED", "Concluída"
        CANCELED = "CANCELED", "Cancelada"
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário", 
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    account = models.ForeignKey(
        FinancialAccount, 
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transactions'
    )
    tags = models.ManyToManyField(
        Tag, 
        blank=True,
        related_name='transactions'
    )
    
    description = models.CharField('Descrição', max_length=200)
    amount = models.DecimalField(
        "Valor",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    type = models.CharField('Tipo', max_length=10, choices=TransactionType.choices)
    date = models.DateField('Data')
    status = models.CharField(
        'Status', 
        max_length=10, 
        choices=TransactionStatus.choices, 
        default='PENDING'
    )
    notes = models.TextField('Observações', blank=True)
    
    # Campos para transferências
    related_transaction = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        help_text="Transação relacionada (para transferências)"
    )
    
    # Campos para conciliação bancária
    bank_statement_id = models.CharField(
        'ID Extrato Bancário',
        max_length=100, 
        blank=True,
        help_text="ID da transação no extrato bancário"
    )
    reconciled_at = models.DateTimeField(
        'Conciliado em',
        null=True, 
        blank=True
    )
    
    # Campos para parcelamento
    installment_number = models.PositiveSmallIntegerField(
        'Número da Parcela',
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)]
    )
    total_installments = models.PositiveSmallIntegerField(
        'Total de Parcelas',
        null=True, 
        blank=True,
        validators=[MinValueValidator(1)]
    )
    parent_transaction = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='installments',
        help_text="Transação pai para parcelamentos"
    )
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'account']),
            models.Index(fields=['status']),
            models.Index(fields=['date', 'type']),
            models.Index(fields=['related_transaction']),
            models.Index(fields=['parent_transaction']),
            models.Index(fields=['user', 'status','date']),
        ]

    
    def __str__(self):
        return f"{self.get_type_display()} - {self.description} ({self.amount})"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()

        if (
            self.type == self.TransactionType.TRANSFER
            and self.related_transaction is None
        ):
            raise ValidationError(
                {
                    "related_transaction":
                        "Transferências devem possuir uma transação relacionada."
                }
            )

        if (
            self.related_transaction
            and self.related_transaction == self
        ):
            raise ValidationError(
                {
                    "related_transaction":
                        "Uma transação não pode apontar para ela mesma."
                }
            )

        if (
            self.installment_number
            and self.total_installments
            and self.installment_number > self.total_installments
        ):
            raise ValidationError(
                {
                    "installment_number":
                        "Número da parcela inválido."
                }
            )
    
