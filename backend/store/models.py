# models.py
from django.db import models
from django.db.models import F
from django.core.validators import RegexValidator

from shortuuid.django_fields import ShortUUIDField

from .enums import (Share,
                    OrderStatus,)

from user.models import User


class Category(models.Model):
    title       = models.CharField(max_length=144)
    thumbnail   = models.ImageField(upload_to='category/')
    description = models.CharField(max_length=255)
    cid         = ShortUUIDField(max_length=10, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title


class Brand(models.Model):
    title       = models.CharField(max_length=144)
    thumbnail   = models.ImageField(upload_to='brand/')
    description = models.CharField(max_length=255)
    bid         = ShortUUIDField(max_length=10, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    def __str__(self):
        return self.title


class Product(models.Model):
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand           = models.ForeignKey(Brand, on_delete=models.CASCADE)
    pid             = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")
    title           = models.CharField(max_length=144)
    thumbnail       = models.ImageField(upload_to='product/')
    old_price       = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price           = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    off             = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    barcode         = models.DecimalField(max_digits=15, decimal_places=0)
    weight          = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock_qty       = models.DecimalField(max_digits=10, decimal_places=0)
    in_stock        = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    actualPrice     = models.GeneratedField(expression=F("price") + F("shipping_amount") - F("off"),
                                            output_field=models.DecimalField(max_digits=12, decimal_places=2),
                                            db_persist=True)

    def gallery(self):
        return Gallery.objects.filter(product=self)

    def feature(self):
        return Feature.objects.filter(product=self)

    def __str__(self):
        return f"The {self.title} from {self.category} and its brand is {self.brand}"


class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title   = models.CharField(max_length=50)
    picture = models.ImageField(upload_to='gallery/')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'

    def __str__(self):
        return self.title


class Feature(models.Model):
    product     = models.ForeignKey(Product, models.CASCADE)
    title       = models.CharField(max_length=25)
    explanation = models.CharField(max_length=25, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Coupon(models.Model):
    title       = models.CharField(max_length=144, unique=True)
    coupon_type = models.PositiveSmallIntegerField(choices=Share.choices(), default=3)
    expiration  = models.DurationField()
    checkout    = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    cid         = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    def __str__(self):
        return self.title


class UserCoupon(models.Model):
    numbers     = RegexValidator(regex=r"^[0-9]*$")
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    coupon      = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    coupon_code = models.CharField(max_length=5, validators=[numbers], unique=True)
    is_used     = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    uc_id       = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    class Meta:
        verbose_name = 'User Coupon'
        verbose_name_plural = 'User Coupons'

    def __str__(self):
        return f"{self.user} {self.coupon.coupon_type}"


class Cart(models.Model):
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    product        = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity       = models.PositiveIntegerField(default=1)
    realPrice      = models.DecimalField(max_digits=12, decimal_places=2)
    added_at       = models.DateTimeField(auto_now_add=True)
    products_price = models.GeneratedField(expression=F("realPrice") * F("quantity"),
                                      output_field=models.DecimalField(max_digits=12, decimal_places=2),
                                      db_persist=True)
    
    def save(self, *args, **kwargs):
        self.realPrice = self.product.actualPrice
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in cart of {self.user.username}"


class Order(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    cart        = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status      = models.PositiveSmallIntegerField(choices=OrderStatus.choices(), default=1)
    oid         = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")
    updated_at  = models.DateTimeField(auto_now=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.cart}"


class OrderItem(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def save(self, *args, **kwargs):
        self.final_price = self.order.total_price
        super().save(*args, **kwargs)


class WishList(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wid        = ShortUUIDField(max_length=20, db_index=True, unique=True, alphabet="0123456789abcdefghij")

    class Meta:
        verbose_name = 'Wish List'
        verbose_name_plural = 'Wish Lists'

    def __str__(self):
        return f"WishList of {self.user.username}"


class WishListItem(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE, related_name='items')
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Wish List Item'
        verbose_name_plural = 'Wish List Items'

    def __str__(self):
        return f"{self.product.title} in wishlist of {self.wishlist.user.username}"
