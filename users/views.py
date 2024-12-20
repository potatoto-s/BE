import secrets
import random
from datetime import timedelta
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .models import EmailVerification
from .serializers import (
    PasswordChangeSerializer,
    PasswordResetSerializer,
    UserCreateSerializer,
    UserDetailSerializer,
    CustomTokenObtainPairSerializer,
    EmailVerificationSerializer
)

User = get_user_model()

class UserCreateView(generics.CreateAPIView):
    """회원가입 뷰"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        verification_code = ''.join(random.choices('0123456789', k=6))
        expires_at = timezone.now() + timedelta(minutes=30)

        EmailVerification.objects.create(
            user=user,
            code=verification_code,
            expires_at=expires_at
        )

        html_message = render_to_string('emails/email_verification.html', {
            'user': user,
            'verification_code': verification_code
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject='회원가입 이메일 인증',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message
        )

        return Response({
            "message": "회원가입이 완료되었습니다. 이메일로 발송된 인증 코드를 입력해주세요.",
            "user_id": user.id
        }, status=status.HTTP_201_CREATED)

class UserDetailView(generics.RetrieveUpdateAPIView):
    """사용자 정보 조회/수정 뷰"""
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserDeleteView(generics.DestroyAPIView):
    """회원 탈퇴 뷰"""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

class EmailVerificationView(APIView):
    """이메일 인증 뷰"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']
        code = serializer.validated_data['code']

        verification = EmailVerification.objects.filter(
            user_id=user_id,
            code=code,
            is_verified=False
        ).first()

        if not verification:
            return Response({"error": "잘못된 인증 코드입니다."}, status=status.HTTP_400_BAD_REQUEST)

        if verification.is_expired():
            return Response({"error": "만료된 인증 코드입니다."}, status=status.HTTP_400_BAD_REQUEST)

        verification.is_verified = True
        verification.save()

        user = verification.user
        user.is_active = True
        user.save()

        return Response({"message": "이메일이 성공적으로 인증되었습니다."})

class PasswordChangeView(APIView):
    """비밀번호 변경 뷰"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({"error": "현재 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."})

class PasswordResetView(APIView):
    """비밀번호 재설정 뷰"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "해당 이메일로 가입된 계정이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        temp_password = ''.join(random.choices(secrets.token_urlsafe(), k=12))
        user.set_password(temp_password)
        user.save()

        html_message = render_to_string('emails/password_reset.html', {
            'user': user,
            'temp_password': temp_password
        })
        plain_message = strip_tags(html_message)

        send_mail(
            subject='임시 비밀번호 발급',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message
        )

        return Response({"message": "임시 비밀번호가 이메일로 발송되었습니다."})

class EmailCheckView(APIView):
    """이메일 중복 확인 뷰"""
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')

        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "유효하지 않은 이메일 형식입니다."}, status=status.HTTP_400_BAD_REQUEST)

        is_available = not User.objects.filter(email=email).exists()
        return Response({"available": is_available})

class NicknameCheckView(APIView):
    """닉네임 중복 확인 뷰"""
    permission_classes = [AllowAny]

    def post(self, request):
        nickname = request.data.get('nickname')

        if not nickname or not (2 <= len(nickname) <= 10):
            return Response({"error": "닉네임은 2~10자 사이여야 합니다."}, status=status.HTTP_400_BAD_REQUEST)

        is_available = not User.objects.filter(nickname=nickname).exists()
        return Response({"available": is_available})

class LoginView(TokenObtainPairView):
    """로그인 뷰"""
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(email=request.data['email'])
            user.last_login_at = timezone.now()
            user.save()
        return response

class LogoutView(APIView):
    """로그아웃 뷰"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "로그아웃되었습니다."})
        except Exception:
            return Response({"error": "잘못된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)