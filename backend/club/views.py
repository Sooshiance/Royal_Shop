from rest_framework import status, views, permissions
from rest_framework.response import Response

from .services import RateService, CommentService
from .serializers import RateSerializer, CommentSerializer

from store.repositories import ProductRepository


class RateListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product_id):
        product = ProductRepository.get_product_by_id(id=product_id)
        rates = RateService.read_all_rate_of_product(product)
        serializer = RateSerializer(rates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RateSerializer(data=request.data)
        if serializer.is_valid():
            rate = RateService.create_rate(serializer.validated_data)
            return Response(RateSerializer(rate).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        comments = CommentService.get_all_comments()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = CommentService.create_comment(serializer.validated_data)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, comment_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = CommentService.update_comment(comment_id, serializer.validated_data)
            return Response(CommentSerializer(comment).data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        CommentService.delete_comment(comment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
