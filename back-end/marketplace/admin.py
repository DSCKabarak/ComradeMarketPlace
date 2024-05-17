from django.contrib import admin
from .models import Category, Product, ProductImage, Comment, SoldProduct, Bookmark

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'sub_category', 'slug', 'created_at', 'updated_at')
    search_fields = ('category_name', 'sub_category')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'merchant', 'price', 'in_stock', 'tag', 'brand', 'created_at', 'updated_at')
    search_fields = ('product_name', 'category__category_name', 'merchant__username', 'brand')
    list_filter = ('category', 'merchant', 'in_stock')
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'description', 'created_at', 'updated_at')
    search_fields = ('product__product_name', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment', 'created_at')
    search_fields = ('user__username', 'product__product_name', 'comment')

@admin.register(SoldProduct)
class SoldProductAdmin(admin.ModelAdmin):
    list_display = ('merchant', 'buyer', 'product', 'sold', 'in_stock', 'created_at', 'updated_at')
    search_fields = ('merchant__username', 'buyer__username', 'product__product_name')
    list_filter = ('sold', 'in_stock')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_id', 'favorite', 'created_at', 'updated_at')
    search_fields = ('user__username', 'product_id__product_name')
    list_filter = ('favorite',)