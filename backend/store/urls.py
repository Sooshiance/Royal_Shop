from django.urls import path

from .views import (AllCategoryGenericView,
                    CategoryGenericView,
                    BrandsGenericView,
                    BrandAPIView,
                    ProductsGenericAPIView,
                    ProductAPIView,)


app_name = "store"

urlpatterns = [
    path("category/", AllCategoryGenericView.as_view()),
    path("category/<str:pk>/", CategoryGenericView.as_view()),
    path("brand/", BrandsGenericView.as_view()),
    path("brand/<str:pk>/", BrandAPIView.as_view()),
    path("product/", ProductsGenericAPIView.as_view()),
    path("product/<str:pk>/", ProductAPIView.as_view()),
]
