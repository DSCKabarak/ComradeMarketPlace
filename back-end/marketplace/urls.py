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
    path("all-products", ProductViewSet.as_view({"get": "get_products"}), name="product-list"),
    path("products", ProductViewSet.as_view({"post": "create_product"}), name="product-create"),
    path("products/update", ProductViewSet.as_view({"put": "update_product"}), name="product-update"),
    path("products/delete", ProductViewSet.as_view({"delete": "delete_product"}), name="product-delete"),
    
    # Comments
    path("product/comments", CommentViewSet.as_view({"get": "get_comments_by_product"}), name="product-comment-list"),
    path("user/comments", CommentViewSet.as_view({"get": "get_comments_by_user"}), name="user-comment-list"),
    path("comments", CommentViewSet.as_view({"post": "post_comment"}), name="comment-create"),
    path("comments/<int:id>", CommentViewSet.as_view({"delete": "delete_comment"}), name="comment-delete"),
    
    # Product Images
    path("product-images/<int:product_id>/images", ProductImageViewSet.as_view({"get": "images"}), name="product-image-list"),
    path("product-images/<int:product_id>/images", ProductImageViewSet.as_view({"post": "create"}), name="product-image-create"),
    path("product-images/<int:product_id>/images", ProductImageViewSet.as_view({"put": "update"}), name="product-image-update"),
    path("product-images/<int:product_id>/images", ProductImageViewSet.as_view({"delete": "destroy"}), name="product-image-delete"),
    
    # Categories
    path("all-categories", CategoryViewSet.as_view({"get": "get_categories"}), name="category-list"),
    path("categories", CategoryViewSet.as_view({"post": "create_category"}), name="category-create"),
    path("categories/<int:product_id>", CategoryViewSet.as_view({"put": "update_category"}), name="category-update"),
    
    # Bookmarks
    path("bookmarks", BookmarkViewSet.as_view({"get": "get_bookmarks"}), name="bookmark-list"),
    path("bookmarks", BookmarkViewSet.as_view({"post": "create_bookmark"}), name="bookmark-create"),
    path("bookmarks/<int:id>", BookmarkViewSet.as_view({"put": "update_bookmark"}), name="bookmark-update"),
    path("bookmarks/<int:id>", BookmarkViewSet.as_view({"delete": "delete_bookmark"}), name="bookmark-delete"),
]
