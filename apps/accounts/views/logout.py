# apps/accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..serializers.logout import LogoutSerializer
from ..services.user import logout_user


class LogoutView(APIView):
    """
    View para logout do usuário.
    
    Invalida o refresh token adicionando-o à blacklist.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout do usuário",
        description="Realiza o logout invalidando o refresh token fornecido.",
        request=LogoutSerializer,
        responses={
            205: OpenApiResponse(description="Logout realizado com sucesso"),
            400: OpenApiResponse(description="Refresh token inválido ou expirado"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            logout_user(serializer.validated_data["refresh"])

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Logout realizado com sucesso."},
            status=status.HTTP_205_RESET_CONTENT,
        )