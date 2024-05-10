from django.urls import path
from .views import AuthViewSet

urlpatterns = [
    path("login", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("logout", AuthViewSet.as_view({"get": "logout"}), name="logout"),
    path("register", AuthViewSet.as_view({"post": "register"}), name="register"),
    path(
        "verify-email",
        AuthViewSet.as_view({"get": "verify_email"}),
        name="verify-email",
    ),
    path(
        "reset-password",
        AuthViewSet.as_view({"post": "reset_password"}),
        name="reset-password",
    ),
    path(
        "send-password-reset-token",
        AuthViewSet.as_view({"post": "send_password_reset_token"}),
        name="send-password-reset-token",
    ),
    path(
        "change-password",
        AuthViewSet.as_view({"post": "change_password"}),
        name="change-password",
    ),
    path("profile", AuthViewSet.as_view({"get": "get_profile"}), name="get-profile"),
    path(
        "profile/update",
        AuthViewSet.as_view({"put": "update_profile"}),
        name="update-profile",
    ),
    path(
        "refresh-token",
        AuthViewSet.as_view({"post": "refresh_token"}),
        name="refresh-token",
    ),
]
