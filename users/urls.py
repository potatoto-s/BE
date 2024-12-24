from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

router = DefaultRouter()
router.register("profile", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("check/email/", views.EmailCheckView.as_view(), name="check-email"),
    path("check/nickname/", views.NicknameCheckView.as_view(), name="check-nickname"),
]
