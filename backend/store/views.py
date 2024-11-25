from rest_framework import (permissions,
                            status,
                            views,
                            response,
                            generics)

from .models import (Product,
                     Cart)
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


class AllCategoryGenericView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryService.get_all_categories()


class CategoryGenericView(views.APIView):
    def get(self, request, pk):
        cat = CategoryService.get_single_category(pk)
        srz = CategorySerializer(cat)
        return response.Response(srz.data, status=status.HTTP_200_OK)


class BrandsGenericView(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = BrandService.get_all_brands()


class BrandAPIView(views.APIView):
    def get(self, request, pk):
        b = BrandService.get_single_brand(pk)
        srz = BrandSerializer(b)
        return response.Response(srz.data, status=status.HTTP_200_OK)


class ProductsGenericAPIView(generics.ListAPIView):
    serializer_class = AllProductSerializer
    queryset = ProductService.get_all_products()


class ProductAPIView(views.APIView):
    def get(self, request, pk):
        p = ProductService.get_single_product(pk)
        srz = ProductSerializer(p)
        return response.Response(srz.data, status=status.HTTP_200_OK)


class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Retrieve the user's cart."""
        user = self.request.user
        cart_items = CartService.get_user_cart(user)
        serializer = CartSerializer(cart_items, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add a product to the cart."""
        user = self.request.user
        product_id = request.data.get('products')
        # print(product_id)
        y = []
        for dictionary in product_id:
            for value in dictionary.values():
                y.append(value)
        print(f"quantity === {y[-1]}")
        q = y[-1]
        print(f"primary key ==== {y[0]}")
        pk = y[0]
        try:
            product = ProductService.get_single_product(pk)
            print(product)
        except Product.DoesNotExist:
            return response.Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item = CartService.add_to_cart(user, product, q)
        serializer = CartSerializer(cart_item)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Remove an item from the cart."""
        user = self.request.user
        try:
            cart_item = CartService.get_cart(pk, user)
            if cart_item.exists():
                CartService.remove_from_cart(cart_item.first())
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return response.Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update the quantity of a cart item."""
        user = self.request.user
        quantity = request.data.get('quantity')
        try:
            cart_item = CartService.get_cart(pk, user)
            if cart_item.exists():
                updated_cart_item = CartService.update_cart_item(cart_item.first(), quantity)
                serializer = CartSerializer(updated_cart_item)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return response.Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
