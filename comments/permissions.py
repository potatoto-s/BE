# comments/permissions.py
from typing import Any

from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthenticatedWithUnauthorized(BasePermission):
    authentication_classes = [JWTAuthentication]

    # 사용자 인증 여부를 확인하는 커스텀 권한

    # - 인증되지 않은 사용자: 401 Unauthorized 반환
    # - 인증된 사용자: 접근 허용

    # Returns:
    # bool: 인증된 사용자인 경우 True

    # Raises:
    # AuthenticationFailed: 인증되지 않은 사용자인 경우 401 반환

    def authenticate(self, request: Request) -> None:
        # 인증 여부 확인
        if not request.user.is_authenticated:
            raise AuthenticationFailed("로그인이 필요합니다.")

    def has_permission(self, request: Request, view: APIView) -> bool:
        # 권한 확인
        self.authenticate(request)
        return True
