from django.urls import path

from .views import (RateCreateView,
                    RateListView,
                    CommentCreateView,
                    CommentListView,
                    CommentUpdateView,
                    CommentDeleteView,
                    HighestProductRateAPIView,)


app_name = "club"

urlpatterns = [
    path('rates/<int:product_id>/', RateListView.as_view(), name='rate-list'),
    path('rates/create/<int:product_id>/', RateCreateView.as_view(), name='rate-create'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/update/<int:pk>/', CommentUpdateView.as_view(), name='comment-update'),
    path('comments/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment-delete'),
    path("rates/highest-product/", HighestProductRateAPIView.as_view(), name='highest-rates'),
]
