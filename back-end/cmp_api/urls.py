from django.urls import path, include
from rest_framework import routers
from cmp_api.views import (
    ProductListAPIView,
    ProductImageViewSet,
    AuthViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('api/product-images', ProductImageViewSet, basename='product-images')

urlpatterns = [
    path(r'', include(router.urls)),
    path('api/products', ProductListAPIView.as_view(), name='products')
]


