# apps/finance/views/budget_view.py

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.finance.serializers.budget_serializer import BudgetSerializer
from apps.finance.services.budget_service import BudgetService


class BudgetViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de orçamentos.
    """

    permission_classes = [
        IsAuthenticated
    ]


    @extend_schema(
        summary="Listar orçamentos",
        description="Retorna todos os orçamentos do usuário autenticado.",
        responses={
            200: BudgetSerializer(many=True),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Budgets"],
    )
    def list(self, request):

        budgets = BudgetService.list(
            user=request.user
        )

        serializer = BudgetSerializer(
            budgets,
            many=True
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Criar orçamento",
        description="Cria um novo orçamento para o usuário autenticado.",
        request=BudgetSerializer,
        responses={
            201: BudgetSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            409: OpenApiResponse(
                description="Orçamento já existe"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Budgets"],
    )
    def create(self, request):

        serializer = BudgetSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        budget = BudgetService.create(
            user=request.user,
            data=serializer.validated_data
        )

        return Response(
            BudgetSerializer(budget).data,
            status=status.HTTP_201_CREATED
        )


    @extend_schema(
        summary="Buscar orçamento",
        description="Retorna um orçamento específico do usuário autenticado.",
        responses={
            200: BudgetSerializer,
            404: OpenApiResponse(
                description="Orçamento não encontrado"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Budgets"],
    )
    def retrieve(self, request, pk=None):

        budget = BudgetService.get_by_id(
            user=request.user,
            budget_id=pk
        )

        serializer = BudgetSerializer(
            budget
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Atualizar orçamento",
        description="Atualiza completamente um orçamento.",
        request=BudgetSerializer,
        responses={
            200: BudgetSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            404: OpenApiResponse(
                description="Orçamento não encontrado"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Budgets"],
    )
    def update(self, request, pk=None):

        budget = BudgetService.get_by_id(
            user=request.user,
            budget_id=pk
        )

        serializer = BudgetSerializer(
            budget,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        budget = BudgetService.update(
            budget,
            serializer.validated_data
        )

        return Response(
            BudgetSerializer(budget).data
        )


    @extend_schema(
        summary="Atualizar parcialmente orçamento",
        description="Atualiza parcialmente um orçamento.",
        request=BudgetSerializer,
        responses={
            200: BudgetSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            404: OpenApiResponse(
                description="Orçamento não encontrado"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Budgets"],
    )
    def partial_update(self, request, pk=None):

        budget = BudgetService.get_by_id(
            user=request.user,
            budget_id=pk
        )

        serializer = BudgetSerializer(
            budget,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )

        budget = BudgetService.update(
            budget,
            serializer.validated_data
        )

        return Response(
            BudgetSerializer(budget).data
        )


    @extend_schema(
        summary="Excluir orçamento",
        description="Exclui um orçamento.",
        responses={
            204: OpenApiResponse(
                description="Orçamento excluído com sucesso"
            ),
            404: OpenApiResponse(
                description="Orçamento não encontrado"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Budgets"],
    )
    def destroy(self, request, pk=None):

        budget = BudgetService.get_by_id(
            user=request.user,
            budget_id=pk
        )

        BudgetService.delete(
            budget
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )