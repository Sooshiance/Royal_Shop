from rest_framework import (permissions,
                            status,
                            views,
                            response,)

from .serializers import (CategorySerializer,
                          BrandSerializer,
                          ProductSerializer,
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

    def get(self, cid=None):
        if cid:
            category = CategoryService.get_single_category(cid)
            srz = CategorySerializer(category)
            return response.Response(srz, status=status.HTTP_200_OK)
        categories = CategoryService.get_all_categories()
        all_srz = CategorySerializer(categories)
        return response.Response(all_srz, status=status.HTTP_200_OK)


class BrandAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, bid=None):
        if bid:
            brand = BrandService.get_single_brand(bid)
            srz = BrandSerializer(brand)
            return response.Response(srz, status=status.HTTP_200_OK)
        brand = BrandService.get_all_brands()
        all_srz = BrandSerializer(brand)
        return response.Response(all_srz, status=status.HTTP_200_OK)


class ProductAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, pid=None):
        if pid:
            product = ProductService.get_single_product(pid)
            srz = ProductSerializer(product)
            return response.Response(srz, status=status.HTTP_200_OK)
        products = ProductService.get_all_products()
        all_srz = ProductSerializer(products)
        return response.Response(all_srz, status=status.HTTP_200_OK)
