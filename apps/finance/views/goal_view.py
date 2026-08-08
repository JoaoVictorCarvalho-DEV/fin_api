from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.finance.serializers.goal_serializer import GoalSerializer, GoalCreateUpdateSerializer
from apps.finance.services.goal_service import GoalService
from apps.finance.exceptions import GoalAlreadyExistsError, GoalNotFoundError


class GoalViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Listar metas",
        description="Retorna todas as metas do usuário autenticado.",
        responses={
            200: GoalSerializer(many=True),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Goals"],
    )
    def list(self, request):
        goals = GoalService.list(user=request.user)
        serializer = GoalSerializer(goals, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Criar meta",
        description="Cria uma nova meta para o usuário autenticado.",
        request=GoalCreateUpdateSerializer,
        responses={
            201: GoalSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            401: OpenApiResponse(description="Usuário não autenticado"),
            409: OpenApiResponse(description="Meta já existe"),
        },
        tags=["Goals"],
    )
    def create(self, request):
        serializer = GoalCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            goal = GoalService.create(user=request.user, data=serializer.validated_data)
        except GoalAlreadyExistsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(GoalSerializer(goal).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Buscar meta",
        description="Retorna uma meta específica do usuário autenticado.",
        responses={
            200: GoalSerializer,
            404: OpenApiResponse(description="Meta não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Goals"],
    )
    def retrieve(self, request, pk=None):
        try:
            goal = GoalService.get_by_id(user=request.user, goal_id=pk)
        except GoalNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        return Response(GoalSerializer(goal).data)

    @extend_schema(
        summary="Atualizar meta",
        description="Atualiza completamente uma meta.",
        request=GoalCreateUpdateSerializer,
        responses={
            200: GoalSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Meta não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Goals"],
    )
    def update(self, request, pk=None):
        try:
            goal = GoalService.get_by_id(user=request.user, goal_id=pk)
        except GoalNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        serializer = GoalCreateUpdateSerializer(goal, data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            goal = GoalService.update(goal, serializer.validated_data)
        except GoalAlreadyExistsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(GoalSerializer(goal).data)

    @extend_schema(
        summary="Atualizar parcialmente meta",
        description="Atualiza parcialmente uma meta.",
        request=GoalCreateUpdateSerializer,
        responses={
            200: GoalSerializer,
            400: OpenApiResponse(description="Dados inválidos"),
            404: OpenApiResponse(description="Meta não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Goals"],
    )
    def partial_update(self, request, pk=None):
        try:
            goal = GoalService.get_by_id(user=request.user, goal_id=pk)
        except GoalNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        serializer = GoalCreateUpdateSerializer(goal, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            goal = GoalService.update(goal, serializer.validated_data)
        except GoalAlreadyExistsError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_409_CONFLICT)

        return Response(GoalSerializer(goal).data)

    @extend_schema(
        summary="Excluir meta",
        description="Exclui uma meta do usuário autenticado.",
        responses={
            204: OpenApiResponse(description="Meta excluída com sucesso"),
            404: OpenApiResponse(description="Meta não encontrada"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Goals"],
    )
    def destroy(self, request, pk=None):
        try:
            goal = GoalService.get_by_id(user=request.user, goal_id=pk)
        except GoalNotFoundError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

        GoalService.delete(goal)

        return Response(status=status.HTTP_204_NO_CONTENT)
