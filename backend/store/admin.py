from django.contrib import admin

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


class GalleryAdmin(admin.TabularInline):
    model = Gallery
    extra = 0


class FeatureAdmin(admin.TabularInline):
    model = Feature
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [GalleryAdmin, FeatureAdmin]


class CouponAdmin(admin.ModelAdmin):
    list_display = ('title', 'coupon_type', 'expiration')


class UserCouponAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used', 'is_active')
    list_filter = ['is_used', 'is_active']
    readonly_fields = ['created_at']


class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'cart']


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'order']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user']


class WishListItemAdmin(admin.ModelAdmin):
    list_display = ['wishlist', 'product']


admin.site.register(Category, CategoryAdmin)

admin.site.register(Brand, BrandAdmin)

admin.site.register(Product, ProductAdmin)

admin.site.register(Coupon, CouponAdmin)

admin.site.register(UserCoupon, UserCouponAdmin)

admin.site.register(Cart, CartAdmin)

admin.site.register(Order, OrderAdmin)

admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(WishList, WishListAdmin)

admin.site.register(WishListItem, WishListItemAdmin)
