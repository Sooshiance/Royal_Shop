# repositories.py
from decimal import Decimal
from django.db import transaction

from rest_framework.exceptions import ValidationError

from .models import (User,
                     Category,
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


class CategoryRepository:
    @staticmethod
    def get_all_categories():
        return Category.objects.all().only("title", "thumbnail")

    @staticmethod
    def get_category_by_id(cid):
        try:
            return Category.objects.get(cid=cid)
        except Exception as e:
            raise ValidationError(e)

    @staticmethod
    def create_category(data):
        category = Category.objects.create(**data)
        category.save()
        return category

    @staticmethod
    def update_category(cid, data):
        try:
            category = Category.objects.get(cid=cid)
        except Exception as e:
            raise ValidationError("no object to update")
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    @staticmethod
    def delete_category(cid):
        try:
            Category.objects.get(cid=cid).delete()
        except Exception as e:
            raise ValidationError(e)


class BrandRepository:
    @staticmethod
    def get_all_brands():
        return Brand.objects.all().only("title", "thumbnail")

    @staticmethod
    def get_brand_by_id(bid):
        try:
            return Brand.objects.get(bid=bid)
        except Exception as e:
            raise ValidationError(e)

    @staticmethod
    def create_brand(data):
        brand = Brand.objects.create(**data)
        brand.save()
        return brand

    @staticmethod
    def update_brand(bid, data):
        try:
            brand = Brand.objects.get(bid=bid)
        except Exception as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(brand, key, value)
        brand.save()
        return brand

    @staticmethod
    def delete_brand(bid):
        try:
            Brand.objects.get(bid=bid).delete()
        except Exception as e:
            raise ValidationError(e)


class ProductRepository:
    @staticmethod
    def get_all_products():
        return Product.objects.all().only("pid", "title", "thumbnail", "old_price", "price")

    @staticmethod
    def get_product_by_id(pid):
        try:
            return Product.objects.get(pid=pid).defer("created_at")
        except Exception as e:
            raise ValidationError(e)

    @staticmethod
    def create_product(data)-> Product:
        product = Product.objects.create(**data)
        product.save()
        return product

    @staticmethod
    def update_product(pid, data):
        try:
            product = Product.objects.get(pid=pid)
        except Exception as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product

    @staticmethod
    def delete_product(pid):
        try:
            Product.objects.get(pid=pid).delete()
        except Exception as e:
            raise ValidationError(e)


class GalleryRepository:
    @staticmethod
    def get_gallery_by_product(product):
        return Gallery.objects.filter(product=product)

    @staticmethod
    def create_gallery_item(data):
        gallery_item = Gallery.objects.create(**data)
        gallery_item.save()
        return gallery_item


class FeatureRepository:
    @staticmethod
    def get_features_by_product(product):
        return Feature.objects.filter(product=product)

    @staticmethod
    def create_feature(data):
        feature = Feature.objects.create(**data)
        feature.save()
        return feature
    
    @staticmethod
    def update_feature(fid, data):
        try:
            feature = Feature.objects.get(id=fid)
        except Exception as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(feature, key, value)
        feature.save()
        return feature


class CouponRepository:
    @staticmethod
    def get_coupon_by_id(coupon_id):
        try:
            return Coupon.objects.get(cid=coupon_id)
        except Exception as e:
            raise ValidationError(e)

    @staticmethod
    def create_coupon(data):
        coupon = Coupon.objects.create(**data)
        coupon.save()
        return coupon
    
    @staticmethod
    def update_coupon(cid, data):
        try:
            coupon = Coupon.objects.get(cid)
            for key, value in data.items():
                setattr(coupon, key, value)
            coupon.save()
            return coupon
        except Exception as e:
            raise ValidationError(e)
    
    @staticmethod
    def delete_coupon(cid):
        try:
            Coupon.objects.delete(cid)
        except Exception as e:
            raise ValidationError(e)


class UserCouponRepository:
    @staticmethod
    def get_user_coupon_by_user(user:User):
        return UserCoupon.objects.get(user=user)
    
    @staticmethod
    def update_user_coupon(uc_id, data):
        try:
            uc = UserCoupon.objects.get(uc_id=uc_id)
        except Exception as e:
            raise ValidationError(e)
        for key, value in data.items():
            setattr(uc, key, value)
        uc.save()
        return uc
    
    @staticmethod
    def check_user_coupon(user:User, code:int):
        try:
            uc:UserCoupon = UserCoupon.objects.filter(user=user, coupon_code=code)
            if uc.coupon_code != code or uc.is_used==True or uc.is_active==False:
                raise ValidationError("No valid coupon")
            c:Decimal = uc.coupon.checkout
            return uc, c
        except Exception as e:
            raise ValidationError(e)
    
    @staticmethod
    def delete_user_coupon(uc_id):
        try:
            UserCoupon.objects.delete(uc_id=uc_id)
        except Exception as e:
            raise ValidationError(e)


class CartRepository:
    @staticmethod
    def get_cart_by_user(user:User):
        return Cart.objects.filter(user=user)

    @staticmethod
    def add_to_cart(user:User, product:Product, quantity:int):
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'quantity': quantity, 'realPrice': product.actualPrice}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    @staticmethod
    def remove_from_cart(cart_item:Cart):
        cart_item.delete()

    @staticmethod
    def update_cart_item(cart_item:Cart, quantity:int):
        cart_item.quantity = quantity
        cart_item.save()
        return cart_item


class OrderRepository:
    @staticmethod
    def create_order(user:User, cart:Cart):
        order = Order.objects.create(user=user, cart=cart, total_price=cart.products_price)
        return order

    @staticmethod
    def get_orders_by_user(user:User):
        # user might have multiple `Order`
        return Order.objects.filter(user=user)

    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.objects.get(oid=order_id)
        except Exception as e:
            raise ValidationError(e)


class OrderItemRepository:
    @staticmethod
    def create_order_item(order:Order, user:User, final_price):
        order_item = OrderItem.objects.create(order=order, user=user, final_price=final_price)
        return order_item

    @staticmethod
    def get_order_items_by_order(order:Order):
        return OrderItem.objects.filter(order=order)
