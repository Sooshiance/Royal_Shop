from django.urls import path

from .views import (AllCategoryGenericView,
                    CategoryGenericView,
                    BrandsGenericView,
                    BrandAPIView,
                    ProductsGenericAPIView,
                    ProductAPIView,
                    CartView,)


app_name = "store"

urlpatterns = [
    path("category/", AllCategoryGenericView.as_view()),
    path("category/<int:pk>/", CategoryGenericView.as_view()),
    path("brand/", BrandsGenericView.as_view()),
    path("brand/<int:pk>/", BrandAPIView.as_view()),
    path("product/", ProductsGenericAPIView.as_view()),
    path("product/<int:pk>/", ProductAPIView.as_view()),

    # TODO: Cart scenarios
    path("cart/", CartView.as_view(), name='cart_create'),
    path("cart/<int:pk>/", CartView.as_view(), name='cart_edit'),
]
