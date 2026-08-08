# apps/finance/views/category_view.py

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.finance.serializers.category_serializer import CategorySerializer
from apps.finance.services.category_service import CategoryService


class CategoryViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de categorias.
    """

    permission_classes = [
        IsAuthenticated
    ]


    @extend_schema(
        summary="Listar categorias",
        description="Retorna todas as categorias do usuário autenticado.",
        responses={
            200: CategorySerializer(many=True),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Categories"],
    )
    def list(self, request):

        categories = CategoryService.list(
            user=request.user
        )

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Criar categoria",
        description="Cria uma nova categoria para o usuário autenticado.",
        request=CategorySerializer,
        responses={
            201: CategorySerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            409: OpenApiResponse(
                description="Categoria já existe"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Categories"],
    )
    def create(self, request):

        serializer = CategorySerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        category = CategoryService.create(
            user=request.user,
            data=serializer.validated_data
        )


        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED
        )


    @extend_schema(
        summary="Buscar categoria",
        description="Retorna uma categoria específica do usuário autenticado.",
        responses={
            200: CategorySerializer,
            404: OpenApiResponse(
                description="Categoria não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Categories"],
    )
    def retrieve(self, request, pk=None):

        category = CategoryService.get_by_id(
            user=request.user,
            category_id=pk
        )

        serializer = CategorySerializer(
            category
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Atualizar categoria",
        description="Atualiza completamente uma categoria.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            404: OpenApiResponse(
                description="Categoria não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Categories"],
    )
    def update(self, request, pk=None):

        category = CategoryService.get_by_id(
            user=request.user,
            category_id=pk
        )


        serializer = CategorySerializer(
            category,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        category = CategoryService.update(
            category,
            serializer.validated_data
        )


        return Response(
            CategorySerializer(category).data
        )


    @extend_schema(
        summary="Atualizar parcialmente categoria",
        description="Atualiza parcialmente uma categoria.",
        request=CategorySerializer,
        responses={
            200: CategorySerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            404: OpenApiResponse(
                description="Categoria não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Categories"],
    )
    def partial_update(self, request, pk=None):

        category = CategoryService.get_by_id(
            user=request.user,
            category_id=pk
        )


        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )


        category = CategoryService.update(
            category,
            serializer.validated_data
        )


        return Response(
            CategorySerializer(category).data
        )


    @extend_schema(
        summary="Desativar categoria",
        description="Desativa uma categoria.",
        responses={
            204: OpenApiResponse(
                description="Categoria desativada com sucesso"
            ),
            404: OpenApiResponse(
                description="Categoria não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Categories"],
    )
    def destroy(self, request, pk=None):

        category = CategoryService.get_by_id(
            user=request.user,
            category_id=pk
        )

        CategoryService.deactivate(
            category
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )