# services.py
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import Cart, Order
from .repositories import (
    BrandRepository,
    CartRepository,
    CategoryRepository,
    CouponRepository,
    FeatureRepository,
    GalleryRepository,
    OrderItemRepository,
    OrderRepository,
    ProductRepository,
    UserCouponRepository,
)


class CategoryService:
    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all_categories()

    @staticmethod
    def get_single_category(pk):
        return CategoryRepository.get_category_by_id(pk)

    @staticmethod
    def create_category(data):
        return CategoryRepository.create_category(data)

    @staticmethod
    def update_category(pk, data):
        return CategoryRepository.update_category(pk, data)

    @staticmethod
    def delete_category(pk):
        return CategoryRepository.delete_category(pk)


class BrandService:
    @staticmethod
    def get_all_brands():
        return BrandRepository.get_all_brands()

    @staticmethod
    def get_single_brand(pk):
        return BrandRepository.get_brand_by_id(pk)

    @staticmethod
    def create_brand(data):
        return BrandRepository.create_brand(data)

    @staticmethod
    def delete_brand(pk):
        return BrandRepository.delete_brand(pk)


class ProductService:
    @staticmethod
    def get_all_products():
        return ProductRepository.get_all_products()

    @staticmethod
    def get_single_product(pk):
        return ProductRepository.get_product_by_id(pk)

    @staticmethod
    def create_product(data):
        return ProductRepository.create_product(data)

    @staticmethod
    def update_product(pk, data):
        return ProductRepository.update_product(pk, data)

    @staticmethod
    def delete_product(pk):
        return ProductRepository.delete_product(pk)


class GalleryService:
    @staticmethod
    def get_gallery_by_product(product):
        return GalleryRepository.get_gallery_by_product(product)

    @staticmethod
    def create_gallery_item(data):
        return GalleryRepository.create_gallery_item(data)


class FeatureService:
    @staticmethod
    def get_features_by_product(product):
        return FeatureRepository.get_features_by_product(product)

    @staticmethod
    def create_feature(data):
        return FeatureRepository.create_feature(data)


class CouponService:
    @staticmethod
    def get_coupon_by_id(cid):
        return CouponRepository.get_coupon_by_id(cid)

    @staticmethod
    def create_coupon(data):
        return CouponRepository.create_coupon(data)


class UserCouponService:
    @staticmethod
    def get_user_coupon(user):
        return UserCouponRepository.get_user_coupon_by_user(user)

    @staticmethod
    def update_coupon(uc_id, data):
        return UserCouponRepository.update_user_coupon(uc_id, data)

    @staticmethod
    def delete_coupon(uc_id):
        return UserCouponRepository.delete_user_coupon(uc_id)

    @staticmethod
    def check_user_coupon(user, code):
        return UserCouponRepository.get_user_coupon_checkout(user, code)


class CartService:
    @staticmethod
    def add_to_cart(user, product, quantity):
        return CartRepository.add_to_cart(user, product, quantity)

    @staticmethod
    def remove_from_cart(cart_item):
        CartRepository.remove_from_cart(cart_item)

    @staticmethod
    def update_cart_item(cart_item, quantity):
        return CartRepository.update_cart_item(cart_item, quantity)

    @staticmethod
    def get_user_cart(user):
        return CartRepository.get_cart_by_user(user)

    @staticmethod
    def get_cart(pk, user):
        return CartRepository.get_cart(pk, user)


class OrderService:
    @staticmethod
    @transaction.atomic
    def place_order(user, cart: Cart, coupon_code=None):
        if not cart.products_price:
            raise ValidationError("Cart cannot be empty")

        # Calculate total price
        total_price = cart.products_price

        # Apply coupon if provided
        if coupon_code:
            try:
                user_coupon = UserCouponRepository.check_user_coupon(user, coupon_code)
                discount = (user_coupon.coupon.checkout / 100) * total_price
                total_price -= discount
                user_coupon.is_used = True
                user_coupon.save()
            except ValidationError as e:
                raise e

        order = Order.objects.create(user=user, cart=cart, total_price=total_price)

        # Create order items based on the cart items
        cart_items = CartRepository.get_cart_by_user(user)

        for item in cart_items:
            OrderItemRepository.create_order_item(
                order=order, user=user, final_price=item.products_price
            )

        return order

    @staticmethod
    def get_user_orders(user):
        return OrderRepository.get_orders_by_user(user)

    @staticmethod
    def get_order_details(order_id):
        return OrderRepository.get_order_by_id(order_id)


class OrderItemService:
    @staticmethod
    def create_order_item(user, price, order):
        return OrderItemRepository.create_order_item(order, user, final_price=price)

    @staticmethod
    def get_order_items(order):
        return OrderItemRepository.get_order_items_by_order(order)

    @staticmethod
    def get_order_item_by_user(user):
        return OrderItemRepository.get_order_item_by_user(user)
