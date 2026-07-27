from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

class Tag(models.Model):
    """
    Tags para etiquetar transações
    """
    
    name = models.CharField('Nome', max_length=50)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name="Usuário",
        on_delete=models.CASCADE,
        related_name='tags'
    )
    
    color = models.CharField(
        "Cor",
        max_length=7,
        default="#000000",
        validators=[
            RegexValidator(
                regex=r"^#[0-9A-Fa-f]{6}$",
                message="Cor hexadecimal inválida.",
            )
        ],
    )
    
    is_active = models.BooleanField(
        "Ativa",
        default=True,
    )
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"],
                name="unique_tag_per_user",
            )
        ]
        indexes = [
            models.Index(fields=["user", "name"]),
        ]
    
    def __str__(self):
        return self.name
