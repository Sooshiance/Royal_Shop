from django.urls import path

from .views import (AllCategoryGenericView,
                    CategoryGenericView,
                    BrandsGenericView,
                    BrandAPIView,
                    ProductsGenericAPIView,
                    ProductAPIView,
                    CartView,
                    OrderListView,
                    OrderDetailView,
                    CreateOrderView,
                    OrderItemListView)


app_name = "store"

urlpatterns = [
    path("category/", AllCategoryGenericView.as_view()),
    path("category/<int:pk>/", CategoryGenericView.as_view()),
    path("brand/", BrandsGenericView.as_view()),
    path("brand/<int:pk>/", BrandAPIView.as_view()),
    path("product/", ProductsGenericAPIView.as_view()),
    path("product/<int:pk>/", ProductAPIView.as_view()),

    # TODO: Cart scenarios
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:pk>/', CartView.as_view(), name='cart-item'),
    path("order/", OrderListView.as_view(), name='order-list'),
    path("order/<int:order_id>/", OrderDetailView.as_view(), name='order-detail'),
    path("create/order/", CreateOrderView.as_view(), name='create-order'),
    path("order-item/list/", OrderItemListView.as_view(), name='order-item'),
]
