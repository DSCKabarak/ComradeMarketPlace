from django.urls import path, include
from rest_framework import routers
from .views import (
    ProductListAPIView,
    AuthViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
urlpatterns = [
    path(r'', include(router.urls)),
    path('products', ProductListAPIView.as_view(), name='products')
]