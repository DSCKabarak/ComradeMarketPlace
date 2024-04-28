from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import BaseUserManager
from rest_framework import serializers
from .models import EmailVerificationToken


User = get_user_model()


class EmptySerializer(serializers.Serializer):
    pass


class AuthUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password")

        user = User.objects.get(email=email)

        if not user:
            raise serializers.ValidationError({"message": "Email not found"})
        if not user.check_password(password):
            raise serializers.ValidationError({"message": "Incorrect password"})
        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user.
    """

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "user_type",
            "password",
            "avatar",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"message": "email is already taken."})

        validate_password(password)

        attrs["email"] = BaseUserManager.normalize_email(email)

        return attrs

    def create(self, validated_data):
        """
        Create a new user instance with the validated data.
        """
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PasswordResetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class RefreshTokenRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True)



class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        token = attrs.get("token")
        if not EmailVerificationToken.objects.filter(token=token).exists():
            raise serializers.ValidationError("Invalid or expired verification token.")
        return attrs


class AccountProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "bio",
            "phone_number",
            "user_type",
            "avatar",
        ]
        def update(self, instance, validated_data):
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.last_name)
            instance.bio = validated_data.get("bio", instance.bio)
            instance.phone_number = validated_data.get("phone_number", instance.phone_number)
            instance.user_type = validated_data.get("user_type", instance.user_type)
            instance.avatar = validated_data.get("avatar", instance.avatar)
            instance.save()
            return instance


class ErrorSerializer(serializers.Serializer):
    error_code = serializers.CharField(required=False)
    error_message = serializers.CharField()
    details = serializers.ListField(child=serializers.DictField(), required=False)


class SuccessSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = serializers.DictField(required=False)
