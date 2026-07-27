from apps.finance.models import Category
from django.shortcuts import get_object_or_404

def list_categories(user):
    """
        Lista as categorias do usuário autenticado.
    """
    return Category.objects.filter(
        user=user,
        is_active=True,
    ).order_by("type", "name")

def get_category(user, category_id):
    """
        Recupera uma categoria do usuário.
    """
    return get_object_or_404(
        Category,
        id=category_id,
        user=user,
    )
    
def create_category(user, validated_data):
    """
    Cria uma categoria para o usuário autenticado.
    """

    if Category.objects.filter(
        user=user,
        name=validated_data["name"],
        type=validated_data["type"],
    ).exists():
        raise ValueError(
            "Já existe uma categoria com esse nome."
        )

    return Category.objects.create(
        user=user,
        **validated_data,
    )
    
def update_category(category, validated_data):
    """
        Atualiza uma categoria para o usuário autenticado.
    """

    for field, value in validated_data.items():
        setattr(category, field, value)

    category.save()

    return category

def delete_category(category):
    """
        Desativa uma categoria.
    """

    category.is_active = False
    category.save()

    return category