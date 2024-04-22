from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import (
    Comment,
    Product,
    ProductImage,
    Category,
    Bookmark,
)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "product", "image", "description", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "merchant",
            "category",
            "product_name",
            "price",
            "in_stock",
            "tag",
            "slug",
            "brand",
            "key_features",
            "description",
            "created_at",
            "updated_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name", "sub_category", "slug"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "product",
            "user",
            "comment",
            "created_at",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_name", "sub_category", "slug"]


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ["user", "product_id", "favorite", "created_at", "updated_at"]
