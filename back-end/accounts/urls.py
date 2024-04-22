from django.urls import path, include
from rest_framework import routers
from .views import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("", AuthViewSet, basename="auth")

urlpatterns = [
    path("login/", AuthViewSet.as_view({"post": "login"}), name="login"),
    path("logout/", AuthViewSet.as_view({"post": "logout"}), name="logout"),
    path("register/", AuthViewSet.as_view({"post": "register"}), name="register"),
    path(
        "password-change/",
        AuthViewSet.as_view({"post": "password_change"}),
        name="password-change",
    ),
    path(
        "profile/",
        AuthViewSet.as_view({"get": "profile", "put": "profile"}),
        name="profile",
    ),
    path("", include(router.urls)),
]
