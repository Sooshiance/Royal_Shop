from django.utils import timezone

from .models import UserCoupon

from user.models import User


def check_coupon_expiration(user_coupons:User):
    user_coupon_queryset = UserCoupon.objects.select_related('coupon').filter(user=user_coupons)

    for user_coupon in user_coupon_queryset:
        
        time_elapsed = timezone.now() - user_coupon.created_at
        
        # Check if the coupon has expired based on `seconds` cause of `DurationField`
        if time_elapsed.total_seconds() > user_coupon.coupon.expiration.total_seconds():
            user_coupon.delete()
