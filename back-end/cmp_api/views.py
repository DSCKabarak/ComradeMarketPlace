from rest_framework.response import Response
from rest_framework  import status, viewsets
from rest_framework.decorators import action
from accounts.utils import get_and_authenticate_user, create_user_account
from django.core.exceptions import ImproperlyConfigured
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout
from .serializers import (
    ProductImageSerializer,
    ProductSerializer,
    EmptySerializer,
    UserLoginSerializer,
    AuthUserSerializer,
    UserRegisterSerializer,
    PasswordChangeSerializer,
    AccountProfileSerializer,
    CommentSerializer,
    CategorySerializer,
    BookmarkSerializer,

    )
from merchant.models import (
    Product,
    ProductImage,
    Category,
    Comment,
    Bookmark,
)

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
        'password_change': PasswordChangeSerializer,
        'profile': AccountProfileSerializer
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['GET', ], detail=False, permission_classes=[IsAuthenticated, ])
    def profile(self, request):
        if request.method == 'GET':
            profile = User.objects.get(email=request.user.email)
            serializer = self.get_serializer(profile)
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            profile = User.objects.get(email=request.user.email)
            serializer = self.get_serializer(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = serializer.data
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Successfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status.HTTP_204_NO_CONTENT)
    
    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['GET', ], detail=False)
    def get_products(self, request):
        products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def create_product(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT', ], detail=False)
    def update_product(self, request):
        product = Product.objects.get(id=request.data.get('id'))
        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['DELETE', ], detail=False)
    def delete_product(self, request):
        product = Product.objects.get(id=request.data.get('id'))
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['GET', ], detail=False)
    def get_comments(self, request):
        comments = Comment.objects.all()
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def post_comment(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT', ], detail=False)
    def update_comment(self, request):
        comment = Comment.objects.get(id=request.data.get('id'))
        serializer = self.get_serializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['DELETE', ], detail=False)
    def delete_comment(self, request):
        comment = Comment.objects.get(id=request.data.get('id'))
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductImageSerializer

    @action(methods=['GET', 'POST', 'PUT', 'DELETE'], detail=True, serializer_class=ProductImageSerializer)
    def images(self, request, pk=None):
        product = self.get_object()

        if request.method == 'GET':
            images = ProductImage.objects.filter(product=product)
            serializer = self.get_serializer(images, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Saving the new image and returning the serialized data 
        # with a 201 status code indicating a successful creation.
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        #Updating an existing product image using PUT method.
        elif request.method == 'PUT':
            product_image = self.get_object()
            serializer = self.get_serializer(product_image, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        #Delete the specific product image
        elif request.method == 'DELETE':
            product_image = self.get_object()
            product_image.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['GET', ], detail=False)
    def get_categories(self, request):
        categories = Category.objects.all()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST', ], detail=False)
    def create_category(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT', ], detail=False)
    def update_category(self, request):
        category = Category.objects.get(id=request.data.get('id'))
        serializer = self.get_serializer(category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkViewSet(viewsets.ModelViewerSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    @action(methods=['GET', ], detail=False)
    def get_bookmarks(self, request):
        bookmark = Bookmark.objects.all()
        serializer = self.get_serializer(Bookmark, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def create_bookmark(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['PUT', ], detail=False)    
    def update_bookmark(self,request):
        bookmark=Bookmark.objects.get(id=request.data.get('id'))
        seriaizer=self.get_serializer    
        serializer = self.get_serializer(bookmark, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(methods=['DELETE', ], detail=False)
    def delete_bookmark(self, request):  
        bookmark = Bookmark.objects.get(id=request.data.get('id'))
        bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)