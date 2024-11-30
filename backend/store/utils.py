from django.utils import timezone

from .models import UserCoupon

from user.models import User


def check_coupon_expiration(user_coupons:User):
    # Fetch user coupons with related Coupon data
    user_coupon_queryset = UserCoupon.objects.select_related('coupon').filter(user__in=user_coupons)

    for user_coupon in user_coupon_queryset:
        
        # Calculate the time difference between now and created_at
        time_elapsed = timezone.now() - user_coupon.created_at
        
        # Check if the coupon has expired based on `seconds` cause of `DurationField`
        if time_elapsed.seconds > user_coupon.coupon.expiration:
            user_coupon.delete()
