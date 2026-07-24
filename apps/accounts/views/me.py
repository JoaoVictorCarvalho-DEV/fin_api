# apps/accounts/views.py

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.accounts.services.user import update_user

from ..serializers.me import MeSerializer


class MeView(APIView):
    """
    View para gerenciar os dados do usuário autenticado.
    
    Permite visualizar e atualizar as informações do perfil do usuário
    atualmente autenticado na requisição.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Obter perfil do usuário",
        description="Retorna os dados completos do perfil do usuário autenticado.",
        responses={
            200: MeSerializer,
            401: OpenApiResponse(
                description="Usuário não autenticado",
            ),
        },
        tags=["Accounts"],
    )
    def get(self, request):
        """
        Retorna os dados do perfil do usuário autenticado.
        
        A resposta inclui todas as informações do usuário como nome, email,
        data de criação, etc.
        """
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Atualizar perfil do usuário",
        description="Atualiza parcialmente os dados do perfil do usuário autenticado. "
                    "Apenas os campos enviados no request serão atualizados.",
        request=MeSerializer,
        responses={
            200: MeSerializer,
            400: OpenApiResponse(
                description="Dados inválidos fornecidos",
            ),
            401: OpenApiResponse(
                description="Usuário não autenticado",
            ),
        },
        tags=["Accounts"],
    )
    def patch(self, request):
        """
        Atualiza parcialmente os dados do perfil do usuário autenticado.
        
        Aceita apenas os campos que serão atualizados (PATCH). Os campos
        não enviados permanecem inalterados.
        """
        serializer = MeSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        
        user = update_user(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(MeSerializer(user).data)