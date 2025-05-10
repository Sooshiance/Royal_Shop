# models.py
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F
from user.models import User

from .enums import (
    OrderStatus,
    Share,
)


class Category(models.Model):
    category_name = models.CharField(max_length=144)
    thumbnail = models.ImageField(upload_to="category/")
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=144)
    thumbnail = models.ImageField(upload_to="brand/")
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.brand_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=144, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(upload_to="product/", blank=True, null=True)
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    off = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    stock_qty = models.DecimalField(max_digits=10, decimal_places=0)
    in_stock = models.BooleanField(default=True)
    actualPrice = models.GeneratedField(
        expression=F("price") + F("shipping_amount") - F("off"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def gallery(self):
        return Gallery.objects.filter(product=self)

    def feature(self):
        return Feature.objects.filter(product=self)

    def __str__(self) -> str:
        return f"{self.category.category_name} and its brand is {self.brand}"


class Gallery(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_gallery"
    )
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to="gallery/")

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"

    def __str__(self) -> str:
        return self.title


class Feature(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name="product_feature")
    title = models.CharField(max_length=25)
    explanation = models.CharField(max_length=25, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class Coupon(models.Model):
    title = models.CharField(max_length=144)
    coupon_type = models.PositiveSmallIntegerField(choices=Share.choices(), default=3)
    expiration = models.DurationField()
    checkout = models.DecimalField(max_digits=12, decimal_places=0, default=0)

    def __str__(self) -> str:
        return self.title


class UserCoupon(models.Model):
    numbers = RegexValidator(regex=r"^[0-9]*$")
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_coupon",
        blank=True,
        null=True,
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, null=True)
    coupon_code = models.CharField(max_length=5, validators=[numbers], unique=True)
    is_used = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Coupon"
        verbose_name_plural = "User Coupons"

    def __str__(self):
        return f"{self.user} {self.coupon.coupon_type}"


class Cart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_cart",
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(default=1)
    realPrice = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    products_price = models.GeneratedField(
        expression=F("realPrice") * F("quantity"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )

    def save(self, *args, **kwargs):
        self.realPrice = self.product.actualPrice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.product_title} in cart of {self.user.username}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, blank=True, null=True
    )
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices(), default=1)

    def __str__(self):
        return f"{self.user} {self.cart}"


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    final_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def save(self, *args, **kwargs):
        self.final_price = self.order.total_price
        super().save(*args, **kwargs)


class WishList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_user",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Wish List"
        verbose_name_plural = "Wish Lists"

    def __str__(self):
        return f"WishList of {self.user.username}"


class WishListItem(models.Model):
    wishlist = models.ForeignKey(
        WishList, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_list",
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="wishlist_item_user",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Wish List Item"
        verbose_name_plural = "Wish List Items"

    def __str__(self):
        return (
            f"{self.product.product_title} in wishlist of {self.wishlist.user.username}"
        )
