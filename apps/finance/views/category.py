from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.finance.exceptions import CategoryNotFoundError
from apps.finance.serializers.category import CategorySerializer
from apps.finance.services.category import (
    create_category,
    list_categories,
    delete_category,
    get_category,
    update_category,
)


class CategoryListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = list_categories(request.user)

        serializer = CategorySerializer(
            categories,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = create_category(
            user=request.user,
            validated_data=serializer.validated_data,
        )

        return Response(
            CategorySerializer(category).data,
            status=status.HTTP_201_CREATED,
        )

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        try:
            category = get_category(request.user, category_id)

        except CategoryNotFoundError:
            return Response(
                {"detail": "Categoria não encontrada."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, category_id):
        category = get_category(
            request.user,
            category_id,
        )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        category = update_category(
            category,
            serializer.validated_data,
        )

        return Response(
            CategorySerializer(category).data
        )

    def delete(self, request, category_id):
        category = get_category(
            request.user,
            category_id,
        )

        delete_category(category)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )