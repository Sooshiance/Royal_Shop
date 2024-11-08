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
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    
    gallery = GallerySerializer(many=True, read_only=True)
    feature = FeatureSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['category',
                  'brand',
                  'pid',
                  'title',
                  'thumbnail',
                  'old_price',
                  'price',
                  'shipping_amount',
                  'off',
                  'barcode',
                  'weight',
                  'stock_qty',
                  'in_stock',
                  'actualPrice',
                  'gallery',
                  'feature',
                  ]


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class UserCouponSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = UserCoupon
        exclude = ['user']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        exclude = ['user', 'products_price']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['user']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'final_price']


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        exclude = ['user']


class WishListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListItem
        fields = "__all__"
