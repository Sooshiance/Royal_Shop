# serializers

from rest_framework import serializers

from .models import (Category,
                     Brand,
                     Product,
                     Gallery,
                     Feature,
                     Coupon,
                     UserCoupon,
                     Cart,
                     Order,
                     OrderItem,
                     WishList,
                     WishListItem,)

from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'pk',
            'category_name',
            'thumbnail',
            'description',
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['pk',
                  'brand_name',
                  'thumbnail',
                  'description',
                  ]


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class AllProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'product_title', 'thumbnail', 'price', 'old_price']


class ProductSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)
    feature = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'brand',
            'product_title',
            'thumbnail',
            'old_price',
            'shipping_amount',
            'description',
            'stock_qty',
            'in_stock',
            'price',
            'off',
            'actualPrice',
            'gallery',
            'feature',
        )


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class UserCouponSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserCoupon
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = ['pk', 'user', 'product', 'quantity', 'realPrice', 'products_price']


class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'final_price']


class WishListSerializer(serializers.ModelSerializer):

    user = UserSerializer(many=True, read_only=True)

    class Meta:
        model = WishList
        exclude = ['user']


class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = "__all__"
