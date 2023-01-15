from django.urls import path, include
from rest_framework import routers
from .views import (
    ProductViewSet,
    AuthViewSet,
    CommentViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('api/products', ProductViewSet, basename='products')
router.register('api/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path(r'', include(router.urls)),
]