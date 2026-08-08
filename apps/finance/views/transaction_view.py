from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.finance.serializers.transaction_serializer import (
    TransactionSerializer,
    TransactionCreateSerializer,
    TransactionUpdateSerializer,
)
from apps.finance.services.transaction_service import TransactionService
from apps.finance.exceptions import TransactionNotFoundError


class TransactionViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciamento de transações financeiras.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Listar transações",
        description="Retorna todas as transações do usuário autenticado.",
        responses={
            200: TransactionSerializer(many=True),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Transactions"],
    )
    def list(self, request):
        transactions = TransactionService.list(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Criar transação",
        description="Cria uma nova transação para o usuário autenticado.",
        request=TransactionCreateSerializer,
        responses={
            201: TransactionSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Transactions"],
    )
    def create(self, request):
        serializer = TransactionCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        transaction_obj = TransactionService.create(
            user=request.user,
            data=serializer.validated_data,
        )

        return Response(
            TransactionSerializer(transaction_obj).data,
            status=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Buscar transação",
        description="Retorna uma transação específica do usuário autenticado.",
        responses={
            200: TransactionSerializer,
            404: OpenApiResponse(description="Transação não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Transactions"],
    )
    def retrieve(self, request, pk=None):
        try:
            transaction_obj = TransactionService.get_by_id(request.user, pk)
        except TransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(TransactionSerializer(transaction_obj).data)

    @extend_schema(
        summary="Atualizar transação",
        description="Atualiza completamente uma transação.",
        request=TransactionUpdateSerializer,
        responses={
            200: TransactionSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Transação não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Transactions"],
    )
    def update(self, request, pk=None):
        try:
            transaction_obj = TransactionService.get_by_id(request.user, pk)
        except TransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionUpdateSerializer(
            transaction_obj,
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        transaction_obj = TransactionService.update(
            transaction_obj,
            serializer.validated_data,
        )

        return Response(TransactionSerializer(transaction_obj).data)

    @extend_schema(
        summary="Atualizar parcialmente transação",
        description="Atualiza parcialmente uma transação.",
        request=TransactionUpdateSerializer,
        responses={
            200: TransactionSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Transação não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Transactions"],
    )
    def partial_update(self, request, pk=None):
        try:
            transaction_obj = TransactionService.get_by_id(request.user, pk)
        except TransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        serializer = TransactionUpdateSerializer(
            transaction_obj,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        transaction_obj = TransactionService.update(
            transaction_obj,
            serializer.validated_data,
        )

        return Response(TransactionSerializer(transaction_obj).data)

    @extend_schema(
        summary="Excluir transação",
        description="Exclui uma transação do usuário autenticado.",
        responses={
            204: OpenApiResponse(description="Transação excluída com sucesso"),
            404: OpenApiResponse(description="Transação não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Transactions"],
    )
    def destroy(self, request, pk=None):
        try:
            transaction_obj = TransactionService.get_by_id(request.user, pk)
        except TransactionNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        TransactionService.delete(transaction_obj)

        return Response(status=status.HTTP_204_NO_CONTENT)
