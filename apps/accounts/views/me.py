# apps/accounts/views.py

from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.services.user import update_user

from ..serializers.me import MeSerializer


class MeView(APIView):

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
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