# apps/accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from ..services.user import create_user
from ..serializers.register import RegisterSerializer


class RegisterView(APIView):
    """
    View para registro de novos usuários.
    
    Permite a criação de uma nova conta de usuário com os dados fornecidos.
    """
    
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        summary="Registrar novo usuário",
        description="Cria uma nova conta de usuário com os dados fornecidos. "
                    "A senha deve atender aos requisitos de segurança.",
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(description="Usuário criado com sucesso"),
            400: OpenApiResponse(description="Dados inválidos ou email/telefone já cadastrados"),
        },
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(serializer.validated_data)

        return Response(
            RegisterSerializer(user).data,
            status=status.HTTP_201_CREATED
        )