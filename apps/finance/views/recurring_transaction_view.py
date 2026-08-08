from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.finance.serializers.recurring_transaction_serializer import (
    RecurringTransactionCreateUpdateSerializer,
    RecurringTransactionSerializer,
)
from apps.finance.services.recurring_transaction_service import RecurringTransactionService
from apps.finance.exceptions import (
    RecurringTransactionAlreadyExistsError,
    RecurringTransactionNotFoundError,
)


class RecurringTransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Listar transações recorrentes",
        description="Retorna todas as transações recorrentes do usuário autenticado.",
        responses={
            200: RecurringTransactionSerializer(many=True),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Recurring Transactions"],
    )
    def list(self, request):
        recurring_transactions = RecurringTransactionService.list(user=request.user)
        serializer = RecurringTransactionSerializer(recurring_transactions, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Criar transação recorrente",
        description="Cria uma nova transação recorrente para o usuário autenticado.",
        request=RecurringTransactionCreateUpdateSerializer,
        responses={
            201: RecurringTransactionSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            401: OpenApiResponse(description="Usuário não autenticado"),
            409: OpenApiResponse(description="Transação recorrente já existe"),
        },
        tags=["Recurring Transactions"],
    )
    def create(self, request):
        serializer = RecurringTransactionCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            recurring_transaction = RecurringTransactionService.create(
                user=request.user,
                data=serializer.validated_data,
            )
        except RecurringTransactionAlreadyExistsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(
            RecurringTransactionSerializer(recurring_transaction).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Buscar transação recorrente",
        description="Retorna uma transação recorrente específica do usuário autenticado.",
        responses={
            200: RecurringTransactionSerializer,
            404: OpenApiResponse(description="Transação recorrente não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Recurring Transactions"],
    )
    def retrieve(self, request, pk=None):
        try:
            recurring_transaction = RecurringTransactionService.get_by_id(request.user, pk)
        except RecurringTransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(RecurringTransactionSerializer(recurring_transaction).data)

    @extend_schema(
        summary="Atualizar transação recorrente",
        description="Atualiza completamente uma transação recorrente.",
        request=RecurringTransactionCreateUpdateSerializer,
        responses={
            200: RecurringTransactionSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Transação recorrente não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Recurring Transactions"],
    )
    def update(self, request, pk=None):
        try:
            recurring_transaction = RecurringTransactionService.get_by_id(request.user, pk)
        except RecurringTransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecurringTransactionCreateUpdateSerializer(
            recurring_transaction,
            data=request.data,
        )
        serializer.is_valid(raise_exception=True)

        try:
            recurring_transaction = RecurringTransactionService.update(
                recurring_transaction,
                serializer.validated_data,
            )
        except RecurringTransactionAlreadyExistsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(RecurringTransactionSerializer(recurring_transaction).data)

    @extend_schema(
        summary="Atualizar parcialmente transação recorrente",
        description="Atualiza parcialmente uma transação recorrente.",
        request=RecurringTransactionCreateUpdateSerializer,
        responses={
            200: RecurringTransactionSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Transação recorrente não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Recurring Transactions"],
    )
    def partial_update(self, request, pk=None):
        try:
            recurring_transaction = RecurringTransactionService.get_by_id(request.user, pk)
        except RecurringTransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        serializer = RecurringTransactionCreateUpdateSerializer(
            recurring_transaction,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        try:
            recurring_transaction = RecurringTransactionService.update(
                recurring_transaction,
                serializer.validated_data,
            )
        except RecurringTransactionAlreadyExistsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(RecurringTransactionSerializer(recurring_transaction).data)

    @extend_schema(
        summary="Excluir transação recorrente",
        description="Exclui uma transação recorrente do usuário autenticado.",
        responses={
            204: OpenApiResponse(description="Transação recorrente excluída com sucesso"),
            404: OpenApiResponse(description="Transação recorrente não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Recurring Transactions"],
    )
    def destroy(self, request, pk=None):
        try:
            recurring_transaction = RecurringTransactionService.get_by_id(request.user, pk)
        except RecurringTransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        RecurringTransactionService.delete(recurring_transaction)

        return Response(status=status.HTTP_204_NO_CONTENT)
