from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
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
        responses={204: "탈퇴 성공", 401: "인증 실패", 403: "권한 없음"},
    )
    def destroy(self, request, *args, **kwargs):
        """회원 탈퇴를 진행합니다."""
        return super().destroy(request, *args, **kwargs)


class SignUpView(generics.CreateAPIView):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="회원가입",
        request_body=UserSignUpSerializer,
        responses={201: UserSignUpSerializer, 400: "잘못된 요청"},
    )
    def post(self, request, *args, **kwargs):
        """새로운 사용자를 생성합니다."""
        return super().post(request, *args, **kwargs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_summary="로그인",
        responses={200: CustomTokenObtainPairSerializer, 401: "인증 실패"},
    )
    def post(self, request, *args, **kwargs):
        """이메일과 비밀번호로 로그인하여 토큰을 발급받습니다."""
        return super().post(request, *args, **kwargs)


class EmailCheckView(generics.CreateAPIView):
    serializer_class = CheckEmailSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="이메일 중복 확인",
        responses={200: "사용 가능한 이메일", 400: "중복된 이메일"},
    )
    def post(self, request, *args, **kwargs):
        """이메일 중복 여부를 확인합니다."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "사용 가능한 이메일입니다."}, status=status.HTTP_200_OK)


class NicknameCheckView(generics.CreateAPIView):
    serializer_class = CheckNicknameSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="닉네임 중복 확인",
        responses={200: "사용 가능한 닉네임", 400: "중복된 닉네임"},
    )
    def post(self, request, *args, **kwargs):
        """닉네임 중복 여부를 확인합니다."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "사용 가능한 닉네임입니다."}, status=status.HTTP_200_OK)
