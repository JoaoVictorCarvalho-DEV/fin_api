# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.logout import LogoutSerializer
from ..services.user import logout_user


class LogoutView(APIView):

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