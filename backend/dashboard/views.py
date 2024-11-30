from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .queries import ProductQuery, RateQuery

from store.models import Product
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

    def get(self, request, threshold_qty:int, status:str):
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


class AdvancedSearchProductAPIView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer

    def get_object(self):
        qr = Q()
        kwargs = self.request.query_params
        product_title = kwargs.get("product_title", None)

        # TODO: You can add more query parameters

        if product_title:
            # TODO: Take care of type casting
            qr &= Q(product_title__icontains=str(product_title))
        
        return qr
    
    def get_queryset(self):
        qr = self.get_object()
        results = Product.objects.filter(qr)
        return results
