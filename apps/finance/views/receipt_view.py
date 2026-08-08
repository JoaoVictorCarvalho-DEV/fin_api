
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from apps.finance.serializers.receipt_serializer import (
    ReceiptSerializer,
    ReceiptCreateSerializer,
    ReceiptUpdateSerializer,
)

from apps.finance.services.receipt_service import (
    ReceiptService,
)

from apps.finance.exceptions.receipt_exceptions import (
    ReceiptNotFoundError,
    ReceiptAlreadyExistsError,
    ReceiptFileRequiredError,
    ReceiptFileAlreadyExistsError,
    OCRProcessingError,
    OCRAlreadyProcessingError,
    OCRNotCompletedError,
)


class ReceiptViewSet(viewsets.ViewSet):
    """
    ViewSet responsável pelos endpoints de recibos.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Lista recibos",
        description=(
            "Retorna todos os recibos pertencentes "
            "ao usuário autenticado."
        ),
        responses={
            200: ReceiptSerializer(many=True),
        },
    )
    def list(self, request):
        """
        Lista os recibos do usuário autenticado.
        """

        receipts = ReceiptService.list(
            request.user
        )

        serializer = ReceiptSerializer(
            receipts,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Busca um recibo",
        description=(
            "Retorna um recibo específico "
            "pertencente ao usuário autenticado."
        ),
        responses={
            200: ReceiptSerializer,
            404: OpenApiResponse(
                description="Recibo não encontrado.",
            ),
        },
    )
    def retrieve(self, request, pk=None):
        """
        Busca um recibo pelo ID.
        """

        try:

            receipt = ReceiptService.get_by_id(
                request.user,
                pk,
            )

            serializer = ReceiptSerializer(
                receipt
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ReceiptNotFoundError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Cria um recibo",
        description=(
            "Cria um novo recibo associado a uma "
            "transação do usuário autenticado."
        ),
        request=ReceiptCreateSerializer,
        responses={
            201: ReceiptSerializer,
            400: OpenApiResponse(
                description="Dados inválidos.",
            ),
            404: OpenApiResponse(
                description="Transação não encontrada.",
            ),
            409: OpenApiResponse(
                description="Recibo ou arquivo já cadastrado.",
            ),
        },
    )
    def create(self, request):
        """
        Cria um novo recibo.
        """

        serializer = ReceiptCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:

            receipt = ReceiptService.create(
                request.user,
                serializer.validated_data,
            )

            response_serializer = ReceiptSerializer(
                receipt
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED,
            )

        except ReceiptNotFoundError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except ReceiptAlreadyExistsError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_409_CONFLICT,
            )

        except ReceiptFileRequiredError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ReceiptFileAlreadyExistsError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_409_CONFLICT,
            )

    @extend_schema(
        summary="Atualiza um recibo",
        description=(
            "Atualiza os dados permitidos de um recibo."
        ),
        request=ReceiptUpdateSerializer,
        responses={
            200: ReceiptSerializer,
            404: OpenApiResponse(
                description="Recibo não encontrado.",
            ),
        },
    )
    def update(self, request, pk=None):
        """
        Atualiza um recibo.
        """

        try:

            receipt = ReceiptService.get_by_id(
                request.user,
                pk,
            )

            serializer = ReceiptUpdateSerializer(
                receipt,
                data=request.data,
            )

            serializer.is_valid(
                raise_exception=True
            )

            receipt = ReceiptService.update(
                receipt,
                serializer.validated_data,
            )

            response_serializer = ReceiptSerializer(
                receipt
            )

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK,
            )

        except ReceiptNotFoundError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Exclui um recibo",
        description=(
            "Exclui um recibo pertencente ao "
            "usuário autenticado."
        ),
        responses={
            204: OpenApiResponse(
                description="Recibo excluído com sucesso.",
            ),
            404: OpenApiResponse(
                description="Recibo não encontrado.",
            ),
        },
    )
    def destroy(self, request, pk=None):
        """
        Exclui um recibo.
        """

        try:

            receipt = ReceiptService.get_by_id(
                request.user,
                pk,
            )

            ReceiptService.delete(
                receipt
            )

            return Response(
                status=status.HTTP_204_NO_CONTENT
            )

        except ReceiptNotFoundError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    @extend_schema(
        summary="Inicia processamento OCR",
        description=(
            "Coloca o recibo na fila para "
            "processamento OCR."
        ),
        responses={
            200: ReceiptSerializer,
            404: OpenApiResponse(
                description="Recibo não encontrado.",
            ),
            409: OpenApiResponse(
                description="OCR já está sendo processado.",
            ),
        },
    )
    def start_ocr(self, request, pk=None):
        """
        Inicia o processamento OCR do recibo.
        """

        try:

            receipt = ReceiptService.get_by_id(
                request.user,
                pk,
            )

            receipt = ReceiptService.start_ocr(
                receipt
            )

            serializer = ReceiptSerializer(
                receipt
            )

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ReceiptNotFoundError as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except (
            OCRAlreadyProcessingError,
            OCRProcessingError,
        ) as exc:

            return Response(
                {
                    "detail": str(exc),
                },
                status=status.HTTP_409_CONFLICT,
            )

