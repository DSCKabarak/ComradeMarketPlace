from rest_framework.serializers import ValidationError
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.models import TokenUser
from rest_framework.decorators import action
from datetime import timedelta
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, logout as auth_logout
from utils.token_generator import token_generator_and_check_if_exists
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    OpenApiResponse,
)
from utils.response_utils import ApiResponse
from .models import EmailVerificationToken, PasswordResetToken
from .serializers import (
    AuthUserSerializer,
    UserRegisterSerializer,
    PasswordResetSerializer,
    ErrorSerializer,
    SuccessSerializer,
    AccountProfileSerializer,
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    PasswordResetTokenSerializer,
    RefreshTokenRequestSerializer,
)


User = get_user_model()
response_handler = ApiResponse()


class AuthViewSet(viewsets.GenericViewSet):
    serializer_classes = {
        "login": AuthUserSerializer,
        "register": UserRegisterSerializer,
        "verify_email": EmailVerificationSerializer,
        "reset_password": PasswordResetSerializer,
        "send_password_reset_token": PasswordResetTokenSerializer,
        "change_password": ChangePasswordSerializer,
        "get_profile": AccountProfileSerializer,
        "update_profile": AccountProfileSerializer,
        "refresh_token": RefreshTokenRequestSerializer,
    }

    def get_permissions(self):
        permission_classes_dict = {
            "login": [AllowAny],
            "register": [AllowAny],
            "verify_email": [AllowAny],
            "reset_password": [AllowAny],
            "send_password_reset_token": [AllowAny],
            "change_password": [IsAuthenticated],
            "get_profile": [IsAuthenticated],
            "update_profile": [IsAuthenticated],
            "refresh_token": [IsAuthenticated],
            "logout": [IsAuthenticated],
        }
        permission_classes = permission_classes_dict.get(self.action, [IsAuthenticated])
        return [permission() for permission in permission_classes]

    @extend_schema(
        operation_id="login",
        request=AuthUserSerializer,
        responses={
            "200": SuccessSerializer,
            "400": ErrorSerializer,
        },
        description="User login",
    )
    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            if not user.is_verified:
                return response_handler.unauthorized(
                    "User's email is not verified.",
                )

        except ValidationError as e:
            return response_handler.unauthorized(
                "email or password is incorrect, please try again."
            )

        except Exception as e:
            return response_handler.server_error(e)
        return response_handler.success(
            "Login successful.",
            {"refresh": str(refresh), "access": str(refresh.access_token)},
        )

    @extend_schema(
        operation_id="register",
        request=UserRegisterSerializer,
        responses={
            "201": SuccessSerializer,
            "400": ErrorSerializer,
            "500": ErrorSerializer,
        },
        description="User registration",
    )
    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def register(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            email_verification_token = token_generator_and_check_if_exists(
                EmailVerificationToken
            )
            EmailVerificationToken.objects.create(
                token=email_verification_token, user=user
            )
            # TODO:: Send Email
            return response_handler.created(
                "User registered successfully.",
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "email_verification_token": email_verification_token,
                },
            )
        except ValidationError as e:
            return response_handler.bad_request(e)
        except Exception as e:
            return response_handler.server_error(e)

    @extend_schema(
        operation_id="verify_user_email",
        parameters=[
            OpenApiParameter(
                name="token",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description="Email verification token",
            )
        ],
        responses={
            "200": SuccessSerializer,
            "400": ErrorSerializer,
            "500": ErrorSerializer,
        },
        description="Verify user email",
    )
    @action(methods=["GET"], detail=False)
    def verify_email(self, request):
        token = request.query_params.get("token")
        serializer = self.get_serializer_class()
        serializer = serializer(data={"token": token})
        serializer.is_valid(raise_exception=True)

        try:
            token = serializer.validated_data["token"]
            email_verification_token = EmailVerificationToken.objects.get(token=token)
            if (
                email_verification_token.created_at + timedelta(hours=24)
            ) > timezone.now():
                user = email_verification_token.user
                user.is_verified = True
                user.save()
                email_verification_token.delete()
                refresh = RefreshToken.for_user(user)
                return response_handler.success(
                    "Login successful.",
                    {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": user.email,
                    },
                )
            else:
                return response_handler.handle_exception_response(
                    "EXPIRED_TOKEN",
                    "Invalid or expired verification token.",
                    status_response=status.HTTP_400_BAD_REQUEST,
                )
        except EmailVerificationToken.DoesNotExist:
            return response_handler.handle_exception_response(
                "INVALID_TOKEN",
                "Invalid or expired verification token.",
                status_response=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return response_handler.handle_exception_response(
                "INTERNAL_SERVER_ERROR",
                "An internal server error occurred",
                e,
                status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        operation_id="get_user_profile",
        responses={"200": AccountProfileSerializer, "404": ErrorSerializer},
        description="Get user profile",
    )
    @action(methods=["GET"], detail=False)
    def get_profile(self, request):
        try:
            profile = User.objects.get(email=request.user.email)
            serializer = self.get_serializer_class()
            serializer = serializer(profile)
            return response_handler.success(
                "User profile retrieved successfully.", serializer.data
            )
        except User.DoesNotExist:
            return response_handler.not_found("User not found.")
        except Exception as e:
            return response_handler.server_error(e)

    @extend_schema(
        operation_id="update_user_profile",
        request=AccountProfileSerializer,
        responses={
            "200": SuccessSerializer(data=AccountProfileSerializer),
            "404": ErrorSerializer,
        },
        description="Update user profile",
    )
    @action(methods=["PUT"], detail=False)
    def update_profile(self, request):
        try:
            profile = User.objects.get(email=request.user.email)
            serializer = self.get_serializer_class()
            request.data["email"] = profile.email
            serializer = serializer(profile, data=request.data, partial=True)
            if not serializer.is_valid(raise_exception=True):
                return response_handler.bad_request(serializer.errors)
            serializer.update(profile, request.data)
            return response_handler.success(
                "User profile updated successfully.", serializer.data
            )
        except ValidationError as e:
            return response_handler.bad_request("Validation Error", str(e))
        except Exception as e:
            return response_handler.server_error(str(e))

    @extend_schema(
        operation_id="change_user_password",
        request=ChangePasswordSerializer,
        responses={"204": None, "400": ErrorSerializer},
        description="Change user password",
    )
    @action(methods=["POST"], detail=False)
    def change_password(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        user = request.user
        try:
            serializer.is_valid(raise_exception=True)
            new_password = serializer.validated_data["new_password"]
            user.set_password(new_password)
            user.save()
            return response_handler.handle_no_content_response(
                "Password changed successfully."
            )
        except ValidationError:
            return response_handler.bad_request(serializer.errors)
        except Exception as e:
            return response_handler.server_error(e)

    @extend_schema(
        operation_id="logout",
        parameters=[
            OpenApiParameter(
                name="refresh",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Refresh token",
            )
        ],
        responses={"200": SuccessSerializer, "500": ErrorSerializer},
        description="User logout",
    )
    @action(methods=["GET"], detail=False)
    def logout(self, request):
        try:
            refresh = request.query_params.get("refresh")
            user = request.user

            tokens = RefreshToken(refresh)
            tokens.blacklist()
            
            token_users = Token.objects.filter(user=user)
            for token_user in token_users:
                token_user.delete()
        except TokenError as e:
            return response_handler.forbidden("Invalid token.")

        except Exception as e:
            return response_handler.server_error(str(e))
        return response_handler.success("Successfully logged out.")

    @extend_schema(
        operation_id="send_user_password_reset_token",
        request=None,
        parameters=[
            OpenApiParameter(
                name="email",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=False,
                description="User email",
            )
        ],
        responses={"200": SuccessSerializer, "404": ErrorSerializer},
        description="Send password reset token",
    )
    @action(methods=["GET"], detail=False)
    def send_password_reset_token(self, request):
        email = request.query_params.get("email")
        serializer = self.get_serializer_class()
        serializer = serializer(data={"email": email})
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            password_reset_token = token_generator_and_check_if_exists(
                PasswordResetToken
            )
            PasswordResetToken.objects.create(user=user, token=password_reset_token)
            # TODO:: Send Email
            return response_handler.success(
                "Password reset token sent to your email.",
                {
                    "token": password_reset_token,
                },
            )
        except User.DoesNotExist:
            return response_handler.not_found("User not found.")

    @extend_schema(
        operation_id="password_reset",
        request=PasswordResetSerializer,
        responses={"204": None, "400": ErrorSerializer},
        description="Reset user password",
    )
    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def reset_password(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data, context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return response_handler.bad_request(serializer.errors)

        user = request.user
        password_reset_token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            token_obj = PasswordResetToken.objects.get(
                user=user, token=password_reset_token
            )
            if (token_obj.created_at + timedelta(hours=24)) > timezone.now():
                user.set_password(new_password)
                user.save()
                token_obj.delete()
                return response_handler.success("Password reset successful.")
            else:
                return response_handler.bad_request(
                    "Invalid or expired password reset token."
                )
        except PasswordResetToken.DoesNotExist:
            return response_handler.bad_request(
                "Invalid or expired password reset token."
            )
        except TypeError as e:
            return response_handler.bad_request(e)
        except Exception as e:
            return response_handler.server_error(e)

    @extend_schema(
        operation_id="refresh_token",
        request=RefreshTokenRequestSerializer,
        responses={
            "200": OpenApiResponse(
                response=SuccessSerializer,
                description="Token refreshed successfully",
            ),
            "400": OpenApiResponse(
                response=ErrorSerializer, description="Invalid refresh token"
            ),
        },
        description="Refresh access token",
    )
    @action(methods=["POST"], detail=False)
    def refresh_token(self, request):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            refresh_token = serializer.validated_data["refresh"]
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return response_handler.success(
                "Access token successfully refreshed.",
                {
                    "token": access_token,
                },
            )
        except TokenError as e:
            return response_handler.bad_request(e)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
