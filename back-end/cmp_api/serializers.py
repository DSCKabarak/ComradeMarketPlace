from rest_framework import serializers
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from rest_framework.authtoken.models import Token
from merchant.models import (
    Product,
    ProductImage,
    SoldProduct,
    ConfirmPurchase,
    Category,
)

User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()


    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'bio', 'phone_number', 'user_type',
        'password', 'avatar', 'created_at', 'updated_at', 'auth_token']
        read_only_fields = ['id', 'is_active', 'is_staff', ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_auth_token(self, obj):
        token = Token.objects.create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'bio', 'phone_number', 'user_type',
        'password', 'avatar', ]
    

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)
    
    def validate_password(self, password):
        password_validation.validate_password(password)
        return password
    

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value
    
    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'bio', 'phone_number', 'user_type',
        'avatar', ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['merchant', 'category', 'product_name', 'price', 'in_stock', 'tag',
        'slug', 'brand', 'key_features', 'description', 'created_at', 'updated_at']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'caption']