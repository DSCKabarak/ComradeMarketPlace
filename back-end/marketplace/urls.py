from django.urls import path
from .views import (
    ProductViewSet,
    CommentViewSet,
    ProductImageViewSet,
    CategoryViewSet,
    BookmarkViewSet,
)

urlpatterns = [
    # Products
    path("products", ProductViewSet.as_view({"get": "get_products"}), name="product-list"),
    path("products", ProductViewSet.as_view({"post": "create_product"}), name="product-create"),
    path("products/<int:pk>", ProductViewSet.as_view({"put": "update_product"}), name="product-update"),
    path("products/<int:pk>", ProductViewSet.as_view({"delete": "delete_product"}), name="product-delete"),
    
    # Comments
    path("comments", CommentViewSet.as_view({"get": "get_comments"}), name="comment-list"),
    path("comments", CommentViewSet.as_view({"post": "post_comment"}), name="comment-create"),
    path("comments/<int:pk>", CommentViewSet.as_view({"put": "update_comment"}), name="comment-update"),
    path("comments/<int:pk>", CommentViewSet.as_view({"delete": "delete_comment"}), name="comment-delete"),
    
    # Product Images
    path("product-images/<int:pk>/images", ProductImageViewSet.as_view({"get": "images"}), name="product-image-list"),
    path("product-images/<int:pk>/images", ProductImageViewSet.as_view({"post": "create"}), name="product-image-create"),
    path("product-images/<int:pk>/images", ProductImageViewSet.as_view({"put": "update"}), name="product-image-update"),
    path("product-images/<int:pk>/images", ProductImageViewSet.as_view({"delete": "destroy"}), name="product-image-delete"),
    
    # Categories
    path("categories", CategoryViewSet.as_view({"get": "get_categories"}), name="category-list"),
    path("categories", CategoryViewSet.as_view({"post": "create_category"}), name="category-create"),
    path("categories/<int:pk>", CategoryViewSet.as_view({"put": "update_category"}), name="category-update"),
    
    # Bookmarks
    path("bookmarks", BookmarkViewSet.as_view({"get": "get_bookmarks"}), name="bookmark-list"),
    path("bookmarks", BookmarkViewSet.as_view({"post": "create_bookmark"}), name="bookmark-create"),
    path("bookmarks/<int:pk>", BookmarkViewSet.as_view({"put": "update_bookmark"}), name="bookmark-update"),
    path("bookmarks/<int:pk>", BookmarkViewSet.as_view({"delete": "delete_bookmark"}), name="bookmark-delete"),
]
