from rest_framework import (permissions,
                            status,
                            views,
                            response,
                            generics,
                            exceptions,)

from .models import Product
from .serializers import (CategorySerializer,
                          BrandSerializer,
                          ProductSerializer,
                          AllProductSerializer,
                          CartSerializer,
                          OrderSerializer,
                          OrderItemSerializer,)
from .repositories import (
    CartRepository,
    OrderRepository,
    OrderItemRepository,
)
from .services import (CategoryService,
                       BrandService,
                       ProductService,
                       CartService,
                       OrderService,
                       OrderItemService)
from .utils import check_coupon_expiration


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
        cart_items = CartRepository.get_cart_by_user(self.request.user)
        serializer = CartSerializer(cart_items, many=True)
        check_coupon_expiration(self.request.user)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        products_data = self.request.data.get('products')
        if not products_data:
            return response.Response({'error': 'No products provided'}, status=status.HTTP_400_BAD_REQUEST)

        product_ids = list(map(lambda x: x['pk'], products_data))
        quantities = list(map(lambda x: x['quantity'], products_data))

        try:
            products = list(map(ProductService.get_single_product, product_ids))
        except Product.DoesNotExist:
            return response.Response({'error': 'One or more products not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_items = list(map(lambda p, q: CartService.add_to_cart(self.request.user, p, q), products, quantities))
        serializer = CartSerializer(cart_items, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        quantity = request.data.get('quantity')
        try:
            quantity = int(quantity)
            cart_item = CartRepository.get_cart(pk)
            if cart_item:
                updated_cart_item = CartRepository.update_cart_item(cart_item, quantity)
                serializer = CartSerializer(updated_cart_item)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return response.Response({'error': cart_item}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cart_item = CartRepository.get_cart(pk)
        try:
            if cart_item:
                CartService.remove_from_cart(cart_item)
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return response.Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = OrderService.get_user_orders(self.request.user)
        serializer = OrderSerializer(orders, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        cart = CartRepository.get_cart_by_user(user=self.request.user).first()
        coupon_code = request.data.get('coupon_code', None)
        if coupon_code:
            try:
                order = OrderService.place_order(user=request.user, cart=cart, coupon_code=coupon_code)
                serializer = OrderSerializer(order)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                order = OrderService.place_order(user=request.user, cart=cart, coupon_code=None)
                serializer = OrderSerializer(order)
                return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            order = OrderService.get_order_details(pk)
            serializer = OrderSerializer(order)
            return response.Response(serializer.data)
        except exceptions.ValidationError as e:
            return response.Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


class OrderItemListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = OrderService.get_order_details(order_id)
            order_items = OrderItemService.get_order_items(order)
            serializer = OrderItemSerializer(order_items, many=True)
            return response.Response(serializer.data)
        except exceptions.ValidationError as e:
            return response.Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
