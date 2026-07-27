from apps.finance.models.category import Category
from apps.finance.exceptions import CategoryNotFoundError, CategoryAlreadyExistsError

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
    category = Category.objects.filter(
    id=category_id,
    user=user,
    is_active=True,
    ).first()

    if category is None:
        raise CategoryNotFoundError()

    return category

def create_category(user, validated_data):
    """
    Cria uma categoria para o usuário autenticado.
    """

    if Category.objects.filter(
        user=user,
        name=validated_data["name"],
        type=validated_data["type"],
    ).exists():
        raise CategoryAlreadyExistsError()

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