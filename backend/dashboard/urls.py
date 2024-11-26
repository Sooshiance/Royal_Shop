from django.urls import path

from .views import (
    ProductListView,
    ProductStockThresholdView,
    HighestProductRate,
)


app_name = "dashboard"

urlpatterns = [
    path("product/list/<str:status>/", ProductListView.as_view(), name='product-list'),
    path("product/tres-hold/<str:status>/", ProductStockThresholdView.as_view(), name='stock-tres-hold'),
    path("product/highest-rate/", HighestProductRate.as_view(), name='highest-rate'),
]
