# apps/finance/views/tag_view.py

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.finance.serializers.tag_serializer import TagSerializer
from apps.finance.services.tag_service import TagService


class TagViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de tags.
    """

    permission_classes = [
        IsAuthenticated
    ]


    @extend_schema(
        summary="Listar tags",
        description="Retorna todas as tags do usuário autenticado.",
        responses={
            200: TagSerializer(many=True),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Tags"],
    )
    def list(self, request):

        tags = TagService.list(
            user=request.user
        )

        serializer = TagSerializer(
            tags,
            many=True
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Criar tag",
        description="Cria uma nova tag para o usuário autenticado.",
        request=TagSerializer,
        responses={
            201: TagSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            409: OpenApiResponse(
                description="Tag já existe"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Tags"],
    )
    def create(self, request):

        serializer = TagSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        tag = TagService.create(
            user=request.user,
            data=serializer.validated_data
        )

        return Response(
            TagSerializer(tag).data,
            status=status.HTTP_201_CREATED
        )


    @extend_schema(
        summary="Buscar tag",
        description="Retorna uma tag específica do usuário autenticado.",
        responses={
            200: TagSerializer,
            404: OpenApiResponse(
                description="Tag não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Tags"],
    )
    def retrieve(self, request, pk=None):

        tag = TagService.get_by_id(
            user=request.user,
            tag_id=pk
        )

        serializer = TagSerializer(
            tag
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Atualizar tag",
        description="Atualiza completamente uma tag.",
        request=TagSerializer,
        responses={
            200: TagSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            404: OpenApiResponse(
                description="Tag não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Tags"],
    )
    def update(self, request, pk=None):

        tag = TagService.get_by_id(
            user=request.user,
            tag_id=pk
        )

        serializer = TagSerializer(
            tag,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        tag = TagService.update(
            tag,
            serializer.validated_data
        )

        return Response(
            TagSerializer(tag).data
        )


    @extend_schema(
        summary="Atualizar parcialmente tag",
        description="Atualiza parcialmente uma tag.",
        request=TagSerializer,
        responses={
            200: TagSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            404: OpenApiResponse(
                description="Tag não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Tags"],
    )
    def partial_update(self, request, pk=None):

        tag = TagService.get_by_id(
            user=request.user,
            tag_id=pk
        )

        serializer = TagSerializer(
            tag,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        tag = TagService.update(
            tag,
            serializer.validated_data
        )

        return Response(
            TagSerializer(tag).data
        )


    @extend_schema(
        summary="Desativar tag",
        description="Desativa uma tag.",
        responses={
            204: OpenApiResponse(
                description="Tag desativada com sucesso"
            ),
            404: OpenApiResponse(
                description="Tag não encontrada"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Tags"],
    )
    def destroy(self, request, pk=None):

        tag = TagService.get_by_id(
            user=request.user,
            tag_id=pk
        )

        TagService.deactivate(
            tag
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )