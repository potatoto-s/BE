from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsOwner
from .serializers import (
    CheckEmailSerializer,
    CheckNicknameSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


class UserViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        # URL에서 pk를 사용하지 않고 현재 인증된 사용자를 반환
        return self.request.user

    @swagger_auto_schema(
        operation_summary="사용자 프로필 조회", responses={200: UserProfileSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """현재 로그인한 사용자의 프로필을 조회합니다."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="사용자 프로필 수정",
        request_body=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: "잘못된 요청",
            401: "인증 실패",
            403: "권한 없음",
        },
    )
    def partial_update(self, request, *args, **kwargs):
        """현재 로그인한 사용자의 프로필을 수정합니다."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="회원 탈퇴",
        responses={
            204: "탈퇴 성공",
            401: "인증 실패",
            403: "권한 없음"
        }
    )
    def destroy(self, request, *args, **kwargs):
        """회원 탈퇴를 진행합니다."""
        return super().destroy(request, *args, **kwargs)
