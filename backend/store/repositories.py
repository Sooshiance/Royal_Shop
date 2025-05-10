# repositories.py
from decimal import Decimal
from typing import Any

from rest_framework.exceptions import NotAcceptable, NotFound, ValidationError

from .models import (
    Brand,
    Cart,
    Category,
    Coupon,
    Feature,
    Gallery,
    Order,
    OrderItem,
    Product,
    User,
    UserCoupon,
    WishList,
    WishListItem,
)


class CategoryRepository:
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    @staticmethod
    def get_category_by_id(pk):
        try:
            return Category.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(e)

    @staticmethod
    def create_category(data):
        category = Category.objects.create(**data)
        category.save()
        return category

    @staticmethod
    def update_category(pk, data):
        try:
            category = Category.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete_category(pk):
        try:
            Category.objects.get(pk=pk).delete()
        except NotFound as e:
            raise ValidationError(e)


class BrandRepository:
    @staticmethod
    def get_all_brands():
        return Brand.objects.all()

    @staticmethod
    def get_brand_by_id(pk: int):
        try:
            return Brand.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(e)

    @staticmethod
    def create_brand(data: dict[str, Any]):
        brand = Brand.objects.create(**data)
        brand.save()
        return brand

    @staticmethod
    def update_brand(pk: int, data: dict[str, Any]):
        try:
            brand = Brand.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(brand, key, value)
        brand.save()
        return brand

    @staticmethod
    def delete_brand(pk: int):
        try:
            Brand.objects.get(pk=pk).delete()
        except NotFound as e:
            raise ValidationError(e)


class ProductRepository:
    @staticmethod
    def get_all_products():
        return Product.objects.all().only(
            "pk", "product_title", "thumbnail", "old_price", "price"
        )

    @staticmethod
    def get_product_by_id(pk: int):
        try:
            return Product.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(e)

    @staticmethod
    def create_product(data: dict[str, Any]) -> Product:
        product = Product.objects.create(**data)
        product.save()
        return product

    @staticmethod
    def update_product(pk: int, data: dict[str, Any]):
        try:
            product = Product.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(pk: int):
        try:
            Product.objects.get(pk=pk).delete()
        except NotFound as e:
            raise ValidationError(e)


class GalleryRepository:
    @staticmethod
    def get_gallery_by_product(product: Product):
        return Gallery.objects.filter(product=product)

    @staticmethod
    def create_gallery_item(data: dict[str, Any]):
        gallery_item = Gallery.objects.create(**data)
        gallery_item.save()
        return gallery_item


class FeatureRepository:
    @staticmethod
    def get_features_by_product(product: Product):
        return Feature.objects.filter(product=product)

    @staticmethod
    def create_feature(data: dict[str, Any]):
        feature = Feature.objects.create(**data)
        feature.save()
        return feature

    @staticmethod
    def update_feature(fid: int, data: dict[str, Any]):
        try:
            feature = Feature.objects.get(pk=fid)
        except NotFound as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(feature, key, value)
        feature.save()
        return feature


class CouponRepository:
    @staticmethod
    def get_coupon_by_id(coupon_id: int):
        try:
            return Coupon.objects.get(pk=coupon_id)
        except NotFound as e:
            raise ValidationError(e)

    @staticmethod
    def create_coupon(data: dict[str, Any]):
        coupon = Coupon.objects.create(**data)
        coupon.save()
        return coupon

    @staticmethod
    def update_coupon(pk: int, data: dict[str, Any]):
        try:
            coupon = Coupon.objects.get(pk)
            for key, value in data.items():
                setattr(coupon, key, value)
            coupon.save()
            return coupon
        except NotFound as e:
            raise ValidationError(e)

    @staticmethod
    def delete_coupon(pk: int):
        try:
            Coupon.objects.delete(pk)
        except NotFound as e:
            raise ValidationError(e)


class UserCouponRepository:
    @staticmethod
    def get_user_coupon_by_user(user: User):
        return UserCoupon.objects.filter(user=user)

    @staticmethod
    def update_user_coupon(uc_id: int, data: dict[str, Any]):
        try:
            uc = UserCoupon.objects.get(pk=uc_id)
        except NotFound as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(uc, key, value)
        uc.save()
        return uc

    @staticmethod
    def check_user_coupon(user: User, code: int):
        try:
            # TODO: First Software engineer principle(each function must have one responsibility)
            uc: UserCoupon = UserCoupon.objects.filter(
                user=user, coupon_code=code
            ).first()
            if uc.coupon_code != code or uc.is_used is True or uc.is_active is False:
                raise ValidationError("No valid coupon")
            return uc
        except NotAcceptable as e:
            raise ValidationError(str(e))

    @staticmethod
    def get_user_coupon_checkout(user: User, code: int):
        try:
            # TODO: First Software engineer principle(each function must have one responsibility)
            x = __class__.check_user_coupon(user, code)
            c: Decimal = x.objects.select_related("coupon").only("checkout")
            return c
        except NotAcceptable as e:
            raise ValidationError(e)

    @staticmethod
    def delete_user_coupon(uc_id: int):
        try:
            UserCoupon.objects.delete(uc_id=uc_id)
        except NotFound as e:
            raise ValidationError(e)


class CartRepository:
    @staticmethod
    def get_cart_by_user(user: User):
        return Cart.objects.filter(user=user)

    @staticmethod
    def get_cart(pk: int):
        try:
            return Cart.objects.get(pk=pk)
        except NotFound as e:
            raise ValidationError(detail=str(e))

    @staticmethod
    def add_to_cart(user: User, product: Product, quantity: int):
        try:
            if product.stock_qty >= quantity:
                cart_item, created = Cart.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={"quantity": quantity, "realPrice": product.actualPrice},
                )
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                return cart_item
        except NotAcceptable as e:
            raise ValidationError(str(e))

    @staticmethod
    def remove_from_cart(cart_item: Cart):
        cart_item.delete()

    @staticmethod
    def update_cart_item(cart_item: Cart, quantity: int):
        try:
            x = cart_item.quantity + quantity
            if cart_item.product.stock_qty >= x:
                cart_item.quantity += quantity
                cart_item.save()
                return cart_item
        except NotAcceptable as e:
            raise ValidationError(str(e))


class OrderRepository:
    @staticmethod
    def create_order(user: User, cart: Cart):
        if not cart.products_price:
            return ValidationError("Cart can not be empty")
        order = Order.objects.create(
            user=user, cart=cart, total_price=cart.products_price
        )
        return order

    @staticmethod
    def get_orders_by_user(user: User):
        return Order.objects.filter(user=user)

    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.objects.get(oid=order_id)
        except NotFound as e:
            raise ValidationError(e)


class OrderItemRepository:
    @staticmethod
    def create_order_item(order: Order, user: User, final_price):
        order_item = OrderItem.objects.create(
            order=order, user=user, final_price=final_price
        )
        return order_item

    @staticmethod
    def get_order_items_by_order(order: Order):
        return OrderItem.objects.filter(order=order)

    @staticmethod
    def get_order_item_by_user(user: User):
        return OrderItem.objects.filter(user=user).first()


class WishListRepositories:
    @staticmethod
    def get_user_wishlist(user: User):
        return WishList.objects.filter(user=user)

    @staticmethod
    def create_wishlist(data: dict[str, Any]):
        return WishListItem.objects.create(**data)


class WishListItemRepositories:
    @staticmethod
    def get_user_wishlist(user: User):
        return WishListItem.objects.filter(user=user)

    @staticmethod
    def create_wishlist(data: dict[str, Any]):
        return WishListItem.objects.create(**data)
