# apps/accounts/views.py

from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    """
    View para autenticação e obtenção de tokens JWT.
    
    Retorna um par de tokens (access e refresh) para o usuário autenticado.
    """

    @extend_schema(
        summary="Login do usuário",
        description="Autentica o usuário e retorna os tokens JWT de acesso e refresh.",
        request=TokenObtainPairSerializer,  # ou LoginSerializer se for customizado
        responses={
            200: OpenApiResponse(description="Login realizado com sucesso"),
            401: OpenApiResponse(description="Credenciais inválidas"),
        },
        tags=["Accounts"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)