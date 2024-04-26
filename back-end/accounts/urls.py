from django.urls import path
from .views import AuthViewSet

urlpatterns = [
    path("login", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("logout", AuthViewSet.as_view({"post": "logout"}), name="logout"),
    path("register", AuthViewSet.as_view({"post": "register"}), name="register"),
    path("verify_email", AuthViewSet.as_view({"post": "verify_email"}), name="verify-email"),
    path("reset_password", AuthViewSet.as_view({"post": "reset_password"}), name="reset-password"),
    path("send_password_reset_token", AuthViewSet.as_view({"post": "send_password_reset_token"}), name="send-password-reset-token"),
    path("change_password", AuthViewSet.as_view({"post": "change_password"}), name="change-password"),
    path("get_profile", AuthViewSet.as_view({"get": "get_profile"}), name="get-profile"),
    path("update_profile", AuthViewSet.as_view({"put": "update_profile"}), name="update-profile"),
]