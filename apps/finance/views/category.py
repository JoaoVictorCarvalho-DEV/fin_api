# apps/accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..serializers.category import CategorySerializer
from ..services.category import list_categories, create_category, get_category, update_category, delete_category
from ..exceptions import CategoryNotFoundError


class CategoryListCreateView(APIView):
    """
    View para listar e criar categorias do usuário.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Listar categorias",
        description="Retorna todas as categorias do usuário autenticado.",
        responses={
            200: CategorySerializer(many=True),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Categories"],
    )
    def get(self, request):
        categories = list_categories(request.user)

        serializer = CategorySerializer(
            categories,
            many=True,
        )

        return Response(serializer.data)

    @extend_schema(
        summary="Criar categoria",
        description="Cria uma nova categoria para o usuário autenticado.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Categories"],
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = create_category(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED,
        )


class CategoryDetailView(APIView):
    """
    View para visualizar, atualizar e deletar uma categoria específica.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Obter categoria",
        description="Retorna os detalhes de uma categoria específica do usuário.",
        responses={
            200: CategorySerializer,
            404: OpenApiResponse(description="Categoria não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Categories"],
    )
    def get(self, request, category_id):
        try:
            category = get_category(request.user, category_id)

        except CategoryNotFoundError:
            return Response(
                {"detail": "Categoria não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    @extend_schema(
        summary="Atualizar categoria",
        description="Atualiza parcialmente os dados de uma categoria específica.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Categoria não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Categories"],
    )
    def patch(self, request, category_id):
        category = get_category(
            request.user,
            category_id,
        )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        category = update_category(
            category,
            serializer.validated_data,
        )

        return Response(
            CategorySerializer(category).data
        )

    @extend_schema(
        summary="Deletar categoria",
        description="Remove uma categoria específica do usuário.",
        responses={
            204: OpenApiResponse(description="Categoria deletada com sucesso"),
            404: OpenApiResponse(description="Categoria não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Categories"],
    )
    def delete(self, request, category_id):
        category = get_category(
            request.user,
            category_id,
        )

        delete_category(category)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )