from django.urls import path

from .views import (RateCreateView,
                    RateListView,
                    CommentCreateView,
                    CommentListView,
                    HighestProductRateAPIView,)


app_name = "club"

urlpatterns = [
    path('rates/<int:product_id>/', RateListView.as_view(), name='rate-list'),
    path('rates/create/<int:product_id>/', RateCreateView.as_view(), name='rate-create'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path("rates/highest-product/", HighestProductRateAPIView.as_view(), name='highest-rates'),
]
