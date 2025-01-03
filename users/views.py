from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .permissions import IsOwner
from .serializers import (
    CheckEmailSerializer,
    CheckNicknameSerializer,
    CustomTokenObtainPairSerializer,
    PasswordChangeSerializer,
    UserProfileSerializer,
    UserSignUpSerializer,
)

User = get_user_model()


class UserViewSet(GenericViewSet, RetrieveModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        return self.request.user

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        """전체 수정은 비활성화"""
        return Response(
            {"detail": "PUT method not allowed, use PATCH instead"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @extend_schema(
        summary="사용자 프로필 조회",
        description="현재 로그인한 사용자의 프로필 정보를 조회합니다.",
        responses={
            200: UserProfileSerializer,
            401: OpenApiResponse(description="인증되지 않은 사용자"),
            403: OpenApiResponse(description="권한 없음"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="사용자 프로필 수정",
        description="현재 로그인한 사용자의 프로필 정보를 수정합니다.",
        request=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: OpenApiResponse(description="잘못된 요청"),
            401: OpenApiResponse(description="인증되지 않은 사용자"),
            403: OpenApiResponse(description="권한 없음"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="회원 탈퇴",
        description="현재 로그인한 사용자의 계정을 삭제합니다.",
        responses={
            204: OpenApiResponse(description="탈퇴 성공"),
            401: OpenApiResponse(description="인증되지 않은 사용자"),
            403: OpenApiResponse(description="권한 없음"),
        },
    )
    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="회원가입",
        description="새로운 사용자 계정을 생성합니다.",
        request=UserSignUpSerializer,
        responses={201: UserProfileSerializer, 400: OpenApiResponse(description="잘못된 요청")},
    )
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="로그인",
        description="이메일과 비밀번호로 로그인하여 액세스 토큰을 발급받습니다.",
        responses={
            200: inline_serializer(
                name="TokenObtainPairResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                    "user": UserProfileSerializer(),
                },
            ),
            401: OpenApiResponse(description="인증 실패"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(
        summary="토큰 갱신",
        description="리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급받습니다.",
        request=inline_serializer(
            name="TokenRefreshRequest", fields={"refresh": serializers.CharField()}
        ),
        responses={
            200: inline_serializer(
                name="TokenRefreshResponse", fields={"access": serializers.CharField()}
            ),
            401: OpenApiResponse(description="유효하지 않은 토큰"),
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DuplicateCheckView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="이메일/닉네임 중복 확인",
        description="이메일 또는 닉네임의 사용 가능 여부를 확인합니다.",
        parameters=[
            {
                "name": "field",
                "type": str,
                "location": "path",
                "description": "확인할 필드 (email 또는 nickname)",
                "required": True,
            }
        ],
        request=inline_serializer(
            name="DuplicateCheckRequest",
            fields={
                "email": serializers.EmailField(required=False),
                "nickname": serializers.CharField(required=False),
            },
        ),
        responses={
            200: inline_serializer(
                name="DuplicateCheckSuccess", fields={"message": serializers.CharField()}
            ),
            400: OpenApiResponse(description="중복된 값 또는 잘못된 요청"),
        },
    )
    def post(self, request, field):
        field_mapping = {
            "email": ("email", CheckEmailSerializer),
            "nickname": ("nickname", CheckNicknameSerializer),
        }

        if field not in field_mapping:
            return Response({"error": "Invalid field"}, status=status.HTTP_400_BAD_REQUEST)

        field_name, serializer_class = field_mapping[field]
        field_value = request.data.get(field_name)

        if not field_value:
            return Response(
                {field_name: f"{field_name}을(를) 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = serializer_class(data={field_name: field_value})
        serializer.is_valid(raise_exception=True)
        return Response({"message": f"사용 가능한 {field}입니다."})


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    @extend_schema(
        summary="비밀번호 변경",
        description="현재 로그인한 사용자의 비밀번호를 변경합니다.",
        request=PasswordChangeSerializer,
        responses={
            200: inline_serializer(
                name="PasswordChangeSuccess", fields={"message": serializers.CharField()}
            ),
            400: OpenApiResponse(description="잘못된 요청"),
            401: OpenApiResponse(description="인증되지 않은 사용자"),
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response(
                {"current_password": "현재 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."})
