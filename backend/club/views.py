from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .services import RateService, CommentService
from .serializers import RateSerializer, CommentSerializer

from store.repositories import ProductRepository


class MyPagination(PageNumberPagination):
    # TODO: This value is up to you
    page_size = 20


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
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        comments = CommentService.get_all_comments()
        paginator = MyPagination()
        result = paginator.paginate_queryset(comments)
        serializer = CommentSerializer(result, many=True)
        return Response(serializer.data)


class CreateCommentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        srz = CommentSerializer(data=request.data)
        if srz.is_valid():
            comment = CommentService.create_comment(srz.validated_data)
            return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, comment_id):
        srz = CommentSerializer(data=request.data)
        if srz.is_valid():
            comment = CommentService.update_comment(comment_id, srz.validated_data)
            return Response(CommentSerializer(comment).data)

        return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        CommentService.delete_comment(comment_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
