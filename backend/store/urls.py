from django.urls import path

from .views import (CategoryAPIView,
                    BrandAPIView,
                    AllProductsGenericAPIView,
                    ProductGenericAPIView,)


app_name = "store"

urlpatterns = [
    path("category/<str:pk>/", CategoryAPIView.as_view(), name='category'),
    path("brand/<str:pk>/", BrandAPIView.as_view(), name='brand'),
    path("all/products/", AllProductsGenericAPIView.as_view(), name='products'),
    path("each/product/<str:pk>/", ProductGenericAPIView.as_view(), name='product'),
]
