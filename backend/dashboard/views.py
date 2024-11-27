from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .queries import ProductQuery, RateQuery

from store.serializers import ProductSerializer


class MyPagination(PageNumberPagination):
    # TODO: This value is up to you
    page_size = 20


class ProductListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, status):
        products = ProductQuery.all_in_stock_product(status)
        paginator = MyPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return Response(serializer.data)


class ProductStockThresholdView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, threshold_qty, status):
        products = ProductQuery.stock_qty_product(threshold_qty, status)
        paginator = MyPagination()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return Response(serializer.data)


class HighestProductRate(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = RateQuery.highest_average_rate_products()
        paginator = MyPagination()
        result_page = paginator.paginate_queryset(products, request)
        srz = ProductSerializer(result_page, many=True)
        return Response(srz.data)
