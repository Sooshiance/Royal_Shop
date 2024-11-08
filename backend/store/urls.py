from django.urls import path

from .views import (CategoryAPIView,
                    BrandAPIView,
                    ProductAPIView,)


app_name = "store"

urlpatterns = [
    path("category/<str:pid>/", CategoryAPIView.as_view(), name='category'),
    path("brand/<str:bid>/", BrandAPIView.as_view(), name='brand'),
    path("product/<str:pid>/", ProductAPIView.as_view(), name='product'),
]
