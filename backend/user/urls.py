from django.urls import path

from .views import (CustomTokenObtainPairView,
                    RegisterView,
                    ProfileView,
                    VerifyOTPView,
                    PasswordResetRequestView,
                    PasswordResetView,
                    UserCouponView,)


app_name = "user"

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path("profile/", ProfileView.as_view(), name='profile'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('user-coupon/timeout/', UserCouponView.as_view(), name='user-coupon'),
]
