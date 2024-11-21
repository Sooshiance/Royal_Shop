from django.urls import path

from .views import (
    ProductListView,
    ProductStockThresholdView,
)


app_name = "dashboard"

urlpatterns = [
    path("product/list/<str:status>/", ProductListView.as_view()),
    path("product/tres-hold/<str:status>/", ProductStockThresholdView.as_view()),
]
