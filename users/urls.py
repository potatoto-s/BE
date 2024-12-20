from django.urls import path
from .views import (
    UserCreateView,
    UserDetailView,
    UserDeleteView,
    EmailVerificationView,
    PasswordChangeView,
    PasswordResetView,
    EmailCheckView,
    NicknameCheckView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    # 회원가입 관련
    path('signup/', UserCreateView.as_view(), name='user_create'),  # 회원가입
    path('email-verification/', EmailVerificationView.as_view(), name='email_verification'),  # 이메일 인증

    # 사용자 정보 관련
    path('user/', UserDetailView.as_view(), name='user_detail'),  # 사용자 정보 조회 및 수정
    path('user/delete/', UserDeleteView.as_view(), name='user_delete'),  # 회원 탈퇴

    # 비밀번호 관련
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),  # 비밀번호 변경
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),  # 비밀번호 재설정

    # 이메일, 닉네임 중복 확인
    path('email-check/', EmailCheckView.as_view(), name='email_check'),  # 이메일 중복 확인
    path('nickname-check/', NicknameCheckView.as_view(), name='nickname_check'),  # 닉네임 중복 확인

    # 로그인, 로그아웃 관련
    path('login/', LoginView.as_view(), name='login'),  # 로그인
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃
]
