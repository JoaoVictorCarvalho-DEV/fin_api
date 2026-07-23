from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..services.user import create_user
from ..serializers.register import RegisterSerializer


class RegisterView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = create_user(serializer.validated_data)

        return Response(
            RegisterSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

