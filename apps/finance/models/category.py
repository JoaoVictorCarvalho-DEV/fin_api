from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Category(models.Model):
    """
    Categorias para organizar transações
    """
    class CategoryType(models.TextChoices):
        INCOME = "INCOME", "Receita"
        EXPENSE = "EXPENSE", "Despesa"
    
    name = models.CharField('Nome', max_length=100)
    type = models.CharField(
        max_length=10,
        choices=CategoryType.choices,
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Usuário",
    )
    color = models.CharField(
        max_length=7,
        validators=[
            RegexValidator(
                r"^#[0-9A-Fa-f]{6}$",
                "Cor hexadecimal inválida."
            )
        ],
    )
    icon = models.CharField('Ícone', max_length=50, blank=True)
    description = models.TextField('Descrição', blank=True)
    is_active = models.BooleanField('Ativo', default=True)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['type', 'name']
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['is_active']),
        ]
    
    constraints = [
        models.UniqueConstraint(
            fields=["user", "name", "type"],
            name="unique_category_per_user",
        )
    ]
    
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
    