from rest_framework.response import Response
from rest_framework import status, viewsets
from django.db.models import Q
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiResponse,
)
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
from utils.response_utils import ApiResponse
from django.contrib.auth import get_user_model
from django.shortcuts import render

Users = get_user_model()
response_handler = ApiResponse()



def api_documentation_view(request):
    return render(request, 'index.html')

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def get_products(self, request):
        user = request.user
        try:
            products = Product.objects.filter(merchant=user)
            serializer = self.get_serializer(products, many=True)
        except Product.DoesNotExist:
            return response_handler.bad_request(message="No products found")
        except Exception as e:
            return response_handler.server_error(message=e)
        return response_handler.success("all found products", serializer.data)

    @extend_schema(
        operation_id="create_product",
        request=serializer_class,
        responses={201: OpenApiResponse(description="Product created successfully")},
    )
    @action(
        methods=["POST"],
        detail=False,
    )
    def create_product(self, request):
        user = request.user
        request.data["merchant"] = user.id
        try:
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return response_handler.bad_request(errors=serializer.errors)
        except Exception as e:
            return response_handler.server_error(message=str(e))
        serializer.save()
        return response_handler.created("Product created successfully", serializer.data)

    @extend_schema(
        operation_id="update_product",
        parameters=[
            OpenApiParameter(
                name="id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Product ID",
            )
        ],
        request=serializer_class,
        responses={200: OpenApiResponse(description="Product updated successfully")},
    )
    @action(
        methods=["PUT"],
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
        return response_handler.success("Product updated successfully", serializer.data)

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
            return response_handler.forbidden(
                message="You are not authorized to perform this action"
            )
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except Exception as e:
            return response_handler.server_error(message=e)
        if user != product.merchant:
            return response_handler.forbidden(
                message="You are not authorized to perform this action"
            )
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
        product_id = request.query_params.get("id")
        if not product_id:
            return response_handler.bad_request(message="Product ID is required")
        try:
            product = Product.objects.get(id=int(product_id))
            comments = Comment.objects.filter(product=product).all()
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except Comment.DoesNotExist:
            return response_handler.bad_request(message="No comments found")
        except Exception as e:
            return response_handler.server_error(message=e)
        if len(comments) == 0:
            return response_handler.success(message="No comments found")
        serializer = self.get_serializer(comments, many=True)
        return response_handler.success("Comments found", serializer.data)

    @action(
        methods=["GET"],
        detail=False,
    )
    def get_comments_by_user(self, request):
        user = request.user
        try:
            comments = Comment.objects.filter(user=user).all()
        except Comment.DoesNotExist:
            return response_handler.bad_request(message="No comments found")
        except Exception as e:
            return response_handler.server_error(message=e)
        if len(comments) == 0:
            return response_handler.success(message="No comments found")
        serializer = self.get_serializer(comments, many=True)
        return response_handler.success("Comments found", serializer.data)

    @extend_schema(
        request=serializer_class,
        responses={201: OpenApiResponse(description="Comment posted successfully")},
    )
    @action(
        methods=["POST"],
        detail=False,
    )
    def post_comment(self, request):
        user = request.user
        product_id = request.data.get("product")
        request.data["user"] = user.id
        try:
            product = Product.objects.get(id=product_id)
            SoldProduct.objects.filter(product=product, merchant=user)
        except Product.DoesNotExist:
            return response_handler.bad_request(message="Product not found")
        except SoldProduct.DoesNotExist:
            return response_handler.forbidden(
                message="You are not authorized to perform this action"
            )
        except Exception as e:
            return response_handler.server_error(message=str(e))
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.created("Comment posted successfully", serializer.data)

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
            if not comment.exists():
                return response_handler.bad_request(message="Comment not found")
        except Exception as e:
            return response_handler.server_error(message=e)
        comment.delete()
        return response_handler.success("Comment deleted successfully")


class ProductImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    @action(detail=False, methods=["GET"])
    def get_images(self, request):
        product_id = request.query_params.get("id")
        if not product_id:
            return response_handler.bad_request(message="Product ID is required")

        try:
            images = ProductImage.objects.filter(product=product_id).all()
            if not images.exists():
                return response_handler.success(message="No images found")
        except Exception as e:
            return response_handler.server_error(message=str(e))
        serializer = self.get_serializer(images, many=True)
        return response_handler.success("Images found", serializer.data)

    @extend_schema(
        request=serializer_class,
        responses={201: OpenApiResponse(description="Image uploaded successfully")},
    )
    @action(
        methods=["POST"],
        detail=False,
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.created("Image uploaded successfully", serializer.data)

    @action(methods=["DELETE"], detail=False)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return response_handler.success("Image deleted successfully")


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

    @extend_schema(
        request=serializer_class,
        responses={201: OpenApiResponse(description="Category created successfully")},
    )
    @action(
        methods=["POST"],
        detail=False,
    )
    def create_category(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request("Bad request", errors=serializer.errors)
        category_name = serializer.validated_data.get("category_name", " ").lower()
        sub_category = serializer.validated_data.get("sub_category", " ").lower()
        if Category.objects.filter(
            Q(category_name__iexact=category_name)
            | Q(sub_category__iexact=sub_category)
        ).exists():
            return response_handler.bad_request("Category already exists")

        serializer.save(category_name=category_name, sub_category=sub_category)
        return response_handler.created(
            "Category created successfully", serializer.data
        )

    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_category(self, request):
        category_id = request.query_params.get("id")
        if not category_id:
            return response_handler.bad_request("Category ID is required")
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
        except Category.DoesNotExist:
            return response_handler.bad_request("Category not found")
        except Exception as e:
            return response_handler.server_error(message=e)
        return response_handler.success("Category deleted successfully")


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
    def get_bookmarks_by_user(self, request):
        bookmarks = Bookmark.objects.filter(user=request.user)
        if not bookmarks.exists():
            return response_handler.bad_request("No bookmarks found")
        serializer = self.get_serializer(bookmarks, many=True)
        return response_handler.success("Bookmarks found", serializer.data)

    @extend_schema(
        request=serializer_class,
        responses={201: OpenApiResponse(description="Bookmark created successfully")},
    )
    @action(
        methods=["POST"],
        detail=False,
    )
    def create_bookmark(self, request):
        request.data["user"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.created(
            "Bookmark created successfully", serializer.data
        )

    @extend_schema(
        request=serializer_class,
        responses={200: OpenApiResponse(description="Bookmark updated successfully")},
    )
    @action(
        methods=["PUT"],
        detail=False,
    )
    def update_bookmark(self, request):
        bookmark = Bookmark.objects.get(id=request.data.get("id"))
        serializer = self.get_serializer(bookmark, data=request.data, partial=True)
        if not serializer.is_valid(raise_exception=True):
            return response_handler.bad_request(errors=serializer.errors)
        serializer.save()
        return response_handler.success(
            "Bookmark updated successfully", serializer.data
        )

    @action(
        methods=[
            "DELETE",
        ],
        detail=False,
    )
    def delete_bookmark(self, request):
        bookmark_id = request.query_params.get("id")
        if not bookmark_id:
            return response_handler.bad_request("Bookmark ID is required")
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
        except Bookmark.DoesNotExist:
            return response_handler.bad_request("Bookmark not found")
        bookmark.delete()
        return response_handler.no_content("Bookmark deleted successfully")
