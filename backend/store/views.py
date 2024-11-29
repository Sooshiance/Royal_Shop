from rest_framework import (permissions,
                            status,
                            views,
                            response,
                            generics)

from .models import (Product,
                     Cart,
                     Order,)
from .serializers import (CategorySerializer,
                          BrandSerializer,
                          ProductSerializer,
                          AllProductSerializer,
                          UserCouponSerializer,
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
        cart_items = CartService.get_user_cart(self.request.user)
        serializer = CartSerializer(cart_items, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Add multiple products to the cart."""
        products_data = request.data.get('products')
        product_ids = list(map(lambda x: x['pk'], products_data))
        quantities = list(map(lambda x: x['quantity'], products_data))

        try:
            products = list(map(ProductService.get_single_product, product_ids))
        except Product.DoesNotExist:
            return response.Response({'error': 'One or more products not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_items = list(map(lambda p, q: CartService.add_to_cart(self.request.user, p, q), products, quantities))
        serializer = CartSerializer(cart_items, many=True)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Remove an item from the cart."""
        try:
            cart_item = CartService.get_cart(pk, self.request.user)
            if cart_item.exists():
                CartService.remove_from_cart(cart_item.first())
                return response.Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return response.Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update the quantity of a cart item."""
        quantity = request.data.get('quantity')
        try:
            cart_item = CartService.get_cart(pk, self.request.user)
            if cart_item.exists():
                updated_cart_item = CartService.update_cart_item(cart_item.first(), quantity)
                serializer = CartSerializer(updated_cart_item)
                return response.Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return response.Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return response.Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class OrderListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = OrderService.get_user_orders(self.request.user)
        serializer = OrderSerializer(orders, many=True)
        return response.Response(serializer.data)


class OrderDetailView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = OrderService.get_order_details(order_id)
        serializer = OrderSerializer(order)
        return response.Response(serializer.data)


class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart_id = request.data.get('cart_id')
        coupon_code = request.data.get('coupon_code', None)
        cart = CartRepository.get_cart(cart_id, self.request.user)
        order = OrderService.place_order(self.request.user, cart, coupon_code)
        serializer = OrderSerializer(order)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemListView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = OrderRepository.get_order_by_id(order_id)
        create_order = OrderItemRepository.create_order_item(order, self.request.user, order.total_price)
        order_items = OrderItemRepository.get_order_items_by_order(order)
        serializer = OrderItemSerializer(order_items, many=True)
        return response.Response(serializer.data)
