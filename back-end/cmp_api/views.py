from rest_framework.views import APIView
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
    AccountProfileSerializer

    )
from merchant.models import (
    Product,
    ProductImage,
    SoldProduct,
    ConfirmPurchase,
    Category,
    CustomUser,
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
        profile = User.objects.get(email=request.user.email)
        serializer = self.get_serializer(profile)
        data = serializer.data
        return Response(data=data, status=status.HTTP_200_OK)

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



class ProductListAPIView(APIView):

    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]
    
    # List all
    def get(self, request, *args, **kwargs):
        """
        List all product items
        """

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        """
        Create product item
        """
        data = {
            'merchant': request.data.get('merchant'),
            'category': request.data.get('category'),
            'product_name': request.data.get('product_name'),
            'price': request.data.get('price'),
            'in_stock': request.data.get('in_stock'),
            'tag': request.data.get('tag'),
            'brand': request.data.get('brand'),
            'key_features': request.data.get('key_features'),
            'description': request.data.get('description'),
        }

        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(methods=['GET', 'POST'], detail=True, serializer_class=ProductImageSerializer)
    def images(self, request, pk=None):
        product = self.get_object()

        if request.method == 'GET':
            images = ProductImage.objects.filter(product=product)
            serializer = self.get_serializer(images, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
