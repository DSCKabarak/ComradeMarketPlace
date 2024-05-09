from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import permissions
from .serializers import (
    ProductImageSerializer,
    ProductSerializer,
    CommentSerializer,
    CategorySerializer,
    BookmarkSerializer,
)
from .models import (
    Product,
    SoldProduct,
    ProductImage,
    Category,
    Comment,
    Bookmark,
)
from accounts.models import CustomUser
from utils.response_utils import ApiResponse
from django.contrib.auth import get_user_model

Users = get_user_model()
response_handler = ApiResponse()

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(
        methods=["GET",],detail=False,)
    def get_products(self, request):
        user = request.user
        try: 
            products = Product.objects.filter(merchant=user)
            serializer = self.get_serializer(products, many=True)
        except  Product.DoesNotExist:
            return response_handler.bad_request(message="No products found")
        except Exception as e:
            return response_handler.server_error(message=e)
        return response_handler.success("all found products",serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def create_product(self, request):
        user = request.user
        request.data["merchant"] = user.id
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return response_handler.created("Product created successfully", serializer.data)
            else:
                return response_handler.bad_request(errors=serializer.errors)
        except Exception as e:
            return response_handler.server_error(message=str(e))     
        serializer.save()
        return response_handler.created("Product created successfully",serializer.data)

    @action(
        methods=[
            "PUT",
        ],
        detail=False,
    )
    def update_product(self, request):
        product_id = request.query_params.get("id")
        user = request.user
        request.data["merchant"] = user.id
        if not product_id:
            return response_handler.bad_request(message="Product ID is required")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except Exception as e:
            return response_handler.server_error(message=e)
        serializer = self.get_serializer(product, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.success("Product updated successfully",serializer.data)

    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_product(self, request):
        user = request.user
        user = Users.objects.get(id=user.id)
        product_id = request.query_params.get("id")
        if not product_id:
            return response_handler.bad_request(message="Product ID is required")
        if user.user_type != "merchant":
            return response_handler.forbidden(message="You are not authorized to perform this action")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except Exception as e:
            return response_handler.server_error(message=e)
        if user != product.merchant:
            return response_handler.forbidden(message="You are not authorized to perform this action")
        product.delete()
        return response_handler.success("Product deleted successfully")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_comments_by_product(self, request):
        product_id = request.query_params.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
            comments = Comment.objects.filter(product=product).all()
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except Comment.DoesNotExist:
            return response_handler.bad_request(message="No comments found")
        except Exception as e:
            return response_handler.server_error(message=e)
        serializer = self.get_serializer(comments, many=True)
        return response_handler.success("Comments found",serializer.data)

    @action(methods=['GET'], detail=False,)
    def get_comments_by_user(self, request):
        user = request.user
        try:
            comments = Comment.objects.filter(user=user).all()
        except Comment.DoesNotExist:
            return response_handler.bad_request(message="No comments found")
        except Exception as e:
            return response_handler.server_error(message=e)
        serializer = self.get_serializer(comments, many=True)
        return response_handler.success("Comments found",serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def post_comment(self, request):
        user = request.user
        product_id = request.data.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
            SoldProduct.objects.filter(product=product, user=user)
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except SoldProduct.DoesNotExist:
            return response_handler.forbidden(message="You are not authorized to perform this action")
        except Exception as e:
            return response_handler.server_error(message=e)
        serializer = self.get_serializer(data=request.data)
        
        
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.created("Comment posted successfully",serializer.data)


    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_comment(self, request):
        user = request.user
        comment_id = request.query_params.get("id")
        if not comment_id:
            return response_handler.bad_request(message="Comment ID is required")
        user = Users.objects.get(id=user.id)
        try:
            comment = Comment.objects.filter(id=comment_id, user=user)
        except Comment.DoesNotExist:
            return response_handler.bad_request(message="Comment not found")
        except Exception as e:
            return response_handler.server_error(message=e)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    @action(detail=False, methods=["GET"])
    def images(self, request):
        product_id = request.query_params.get('product_id')
        if not product_id:
            return response_handler.bad_request(message="Product ID is required")

        try:
            images = ProductImage.objects.filter(product=product_id).all()
        except ProductImage.DoesNotExist:
            return response_handler.bad_request(message="No images found")
        serializer = self.get_serializer(images, many=True)
        return response_handler.success("Images found",serializer.data)

    @action(methods=["GET"], detail=False)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.created("Image uploaded successfully",serializer.data)

    @action(methods=["PUT"], detail=False)
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.success("Image updated successfully",serializer.data)


    @action(methods=["DELETE"], detail=False)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return response_handler.no_content("Image deleted successfully")


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_categories(self, request):
        categories = Category.objects.all()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def create_category(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request("Bad request", errors=serializer.errors)
        serializer.save()
        return response_handler.created("Category created successfully",serializer.data)

    @action(
        methods=[
            "PUT",
        ],
        detail=False,
    )
    def update_category(self, request):
        category = Category.objects.get(id=request.data.get("id"))
        serializer = self.get_serializer(category, data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request("Bad request",errors=serializer.errors)
        serializer.save()
        return response_handler.success("Category updated successfully",serializer.data)
        


class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_bookmarks(self, request):
        bookmark = Bookmark.objects.filter(user=request.user)
        serializer = self.get_serializer(Bookmark, many=True)
        return response_handler.success("Bookmarks found",serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def create_bookmark(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.created("Bookmark created successfully",serializer.data)
        

    @action(
        methods=[
            "PUT",
        ],
        detail=False,
    )
    def update_bookmark(self, request):
        bookmark = Bookmark.objects.get(id=request.data.get("id"))
        serializer = self.get_serializer(bookmark, data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.success("Bookmark updated successfully",serializer.data)
        

    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_bookmark(self, request):
        bookmark = Bookmark.objects.get(id=request.data.get("id"))
        bookmark.delete()
        return response_handler.no_content("Bookmark deleted successfully")
