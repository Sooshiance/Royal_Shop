from django.urls import path

from .views import (RateListView,
                    CommentListView,
                    CommentDetailView,)


app_name = "club"

urlpatterns = [
    path('rate/product/<str:product_id>/', RateListView.as_view(), name='rate-list'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/<str:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),
]
