from rest_framework import (permissions,
                            status,
                            views,
                            response,
                            generics)

from .models import Product
from .serializers import (CategorySerializer,
                          BrandSerializer,
                          ProductSerializer,
                          AllProductSerializer,
                          UserCouponSerializer,
                          CartSerializer,
                          OrderSerializer,
                          OrderItemSerializer,)
from .services import (CategoryService,
                       BrandService,
                       ProductService,
                       UserCouponService,
                       CartService,
                       OrderService,
                       OrderItemService,)


class CategoryAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, pk=None):
        if pk:
            category = CategoryService.get_single_category(pk)
            srz = CategorySerializer(category)
            return response.Response(srz, status=status.HTTP_200_OK)
        categories = CategoryService.get_all_categories()
        all_srz = CategorySerializer(categories)
        return response.Response(all_srz, status=status.HTTP_200_OK)


class BrandAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, pk=None):
        if pk:
            brand = BrandService.get_single_brand(pk)
            srz = BrandSerializer(brand)
            return response.Response(srz, status=status.HTTP_200_OK)
        brand = BrandService.get_all_brands()
        all_srz = BrandSerializer(brand)
        return response.Response(all_srz, status=status.HTTP_200_OK)


class AllProductsGenericAPIView(generics.ListAPIView):
    serializer_class = AllProductSerializer
    
    def get_queryset(self):
        p = ProductService.get_all_products()
        return p


class ProductGenericAPIView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer

    def get_object(self):
        pk = self.kwargs['pk']
        print(f"get object method ===== {pk}")
        return pk

    def get_queryset(self, request, *args, **kwargs):
        pk = self.get_object()
        print(f"get query set method ==== {pk}")
        try:
            p = Product.objects.get(pk=pk)
        except Exception as e:
            raise 
        print(p.barcode)
        p_srz = ProductSerializer(p)
        return response.Response(p_srz.data, status=status.HTTP_200_OK)
