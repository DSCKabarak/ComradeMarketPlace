from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from accounts.utils import get_and_authenticate_user, create_user_account
from django.core.exceptions import ImproperlyConfigured
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout
from .serializers import (
    ProductSerializer,
    ProductImageSerializer,
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
    

class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return self.queryset.filter(merchant=self.request.user)
    
    @action(methods=['GET'], detail=True)
    def images(self, request, pk=None):
        product = self.get_object()
        images = ProductImage.objects.filter(product=product)
        serializer = ProductImageSerializer(images, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @action(methods=['POST'], detail=True)
    def images(self, request, pk=None):
        product = self.get_object()
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
