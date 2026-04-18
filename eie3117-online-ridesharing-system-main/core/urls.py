from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RouteViewSet, BookingViewSet, get_csrf_token,
    register_view, login_view, logout_view, current_user_view
)

router = DefaultRouter()
router.register(r"routes", RouteViewSet)
router.register(r"bookings", BookingViewSet, basename="booking")

urlpatterns = [
    path("csrf/", get_csrf_token, name="csrf"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("user/", current_user_view, name="current_user"),
    path("", include(router.urls)),
]
