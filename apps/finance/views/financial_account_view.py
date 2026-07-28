from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.finance.exceptions.financial_account_exceptions import (
    FinancialAccountNotFoundError,
    FinancialAccountAlreadyExistsError,
)

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from apps.finance.serializers.financial_account_serializer import (
    FinancialAccountSerializer,
    FinancialAccountCreateUpdateSerializer,
)

from apps.finance.services.financial_account_service import (
    FinancialAccountService,
)


class FinancialAccountViewSet(viewsets.ViewSet):
    """
    Gerenciamento de contas financeiras.
    """

    permission_classes = [
        IsAuthenticated
    ]


    @extend_schema(
        summary="Listar contas financeiras",
        description="Retorna todas as contas financeiras do usuário autenticado.",
        responses={
            200: FinancialAccountSerializer(many=True),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Financial Accounts"],
    )
    def list(self, request):

        accounts = FinancialAccountService.list(
            user=request.user
        )

        serializer = FinancialAccountSerializer(
            accounts,
            many=True
        )

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Buscar conta financeira",
        description="Retorna uma conta financeira específica.",
        responses={
            200: FinancialAccountSerializer,
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
        },
        tags=["Financial Accounts"],
    )
    
    def retrieve(self, request, pk=None):

        try:
            account = FinancialAccountService.get_by_id(
                user=request.user,
                account_id=pk
            )

        except FinancialAccountNotFoundError as error:

            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_404_NOT_FOUND
            )


        serializer = FinancialAccountSerializer(account)

        return Response(
            serializer.data
        )


    @extend_schema(
        summary="Criar conta financeira",
        description="Cria uma nova conta financeira.",
        request=FinancialAccountCreateUpdateSerializer,
        responses={
            201: FinancialAccountSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            409: OpenApiResponse(
                description="Conta já existente"
            ),
        },
        tags=["Financial Accounts"],
    )
    def create(self, request):

        serializer = FinancialAccountCreateUpdateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        try:

            account = FinancialAccountService.create(
                user=request.user,
                validated_data=serializer.validated_data
            )

        except FinancialAccountAlreadyExistsError as error:

            return Response(
                {
                    "detail": str(error)
                },
                status=status.HTTP_409_CONFLICT
            )


        return Response(
            FinancialAccountSerializer(account).data,
            status=status.HTTP_201_CREATED
        )


    @extend_schema(
        summary="Atualizar conta financeira",
        description="Atualiza todos os dados de uma conta.",
        request=FinancialAccountCreateUpdateSerializer,
        responses={
            200: FinancialAccountSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            404: OpenApiResponse(
                description="Conta não encontrada"
            ),
        },
        tags=["Financial Accounts"],
    )
    def update(self, request, pk=None):

        account = FinancialAccountService.get_by_id(
            user=request.user,
            account_id=pk
        )


        serializer = FinancialAccountCreateUpdateSerializer(
            account,
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        account = FinancialAccountService.update(
            account,
            serializer.validated_data
        )


        return Response(
            FinancialAccountSerializer(account).data
        )


    @extend_schema(
        summary="Atualizar parcialmente conta financeira",
        description="Atualiza parcialmente uma conta.",
        request=FinancialAccountCreateUpdateSerializer,
        responses={
            200: FinancialAccountSerializer,
            400: OpenApiResponse(
                description="Dados inválidos"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            404: OpenApiResponse(
                description="Conta não encontrada"
            ),
        },
        tags=["Financial Accounts"],
    )
    def partial_update(self, request, pk=None):

        account = FinancialAccountService.get_by_id(
            user=request.user,
            account_id=pk
        )


        serializer = FinancialAccountCreateUpdateSerializer(
            account,
            data=request.data,
            partial=True
        )

        serializer.is_valid(
            raise_exception=True
        )


        account = FinancialAccountService.update(
            account,
            serializer.validated_data
        )


        return Response(
            FinancialAccountSerializer(account).data
        )


    @extend_schema(
        summary="Desativar conta financeira",
        description="Desativa uma conta financeira.",
        responses={
            204: OpenApiResponse(
                description="Conta desativada com sucesso"
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado"
            ),
            404: OpenApiResponse(
                description="Conta não encontrada"
            ),
        },
        tags=["Financial Accounts"],
    )
    def destroy(self, request, pk=None):

        account = FinancialAccountService.get_by_id(
            user=request.user,
            account_id=pk
        )

        FinancialAccountService.delete(account)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )