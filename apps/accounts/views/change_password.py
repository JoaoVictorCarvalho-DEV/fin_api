# apps/accounts/views.py

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..serializers.change_password import ChangePasswordSerializer
from ..services.user import change_password


class ChangePasswordView(APIView):
    """
    View para alteração de senha do usuário autenticado.
    
    Permite que o usuário altere sua senha fornecendo a senha atual
    e a nova senha. A nova senha deve atender aos requisitos de
    segurança configurados no Django.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Alterar senha do usuário",
        description=(
            "Altera a senha do usuário autenticado. Requer a senha atual "
            "e uma nova senha que atenda aos requisitos de segurança "
            "(mínimo 8 caracteres, não pode ser muito comum, etc)."
        ),
        request=ChangePasswordSerializer,
        responses={
            200: OpenApiResponse(description="Senha alterada com sucesso"),
            400: OpenApiResponse(description="Senha atual incorreta ou nova senha inválida"),
            401: OpenApiResponse(description="Usuário não autenticado"),
        },
        tags=["Accounts"],
    )
    def post(self, request):
        """
        Processa a solicitação de alteração de senha.
        """
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            change_password(
                request.user,
                serializer.validated_data["old_password"],
                serializer.validated_data["new_password"],
            )

        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except ValidationError as exc:
            return Response(
                {"new_password": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Senha alterada com sucesso."},
            status=status.HTTP_200_OK,
        )