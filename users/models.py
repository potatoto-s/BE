from core.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """
    사용자 모델
    """
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    email = models.EmailField(unique=True)
    nickname = models.CharField(
        max_length=10,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text="2~10자의 닉네임을 입력하세요.",
    )
    profile_image = models.ImageField(
        upload_to="profiles/%Y/%m/%d/", null=True, blank=True
    )
    phone = models.CharField(max_length=20, unique=True)

    # 사용자 역할
    ROLE_CHOICES = [
        ("company", "기업"),
        ("workshop", "공방 사장님"),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        help_text="기업 회원 또는 공방 사장님을 선택하세요.",
    )

    # 추가 정보
    company_name = models.CharField(max_length=255, null=True, blank=True)
    workshop_name = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=20, null=True, blank=True)  # 구
    neighborhood = models.CharField(max_length=20, null=True, blank=True)  # 동
    status = models.CharField(
        max_length=20,
        choices=[("active", "활성"), ("inactive", "비활성"), ("suspended", "정지")],
        default="active",
    )
    status_changed_at = models.DateTimeField(null=True, blank=True)
    status_reason = models.TextField(null=True, blank=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    # 알림 설정
    push_enabled = models.BooleanField(default=True)
    message_notification = models.BooleanField(default=True)
    friend_notification = models.BooleanField(default=True)
    comment_notification = models.BooleanField(default=True)
    like_notification = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "nickname", "role"]

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        permissions = [
            ("can_view_profile", "Can view profile"),
        ]

    def __str__(self):
        return self.nickname


class UserProfile(TimeStampedModel):
    """
    사용자 프로필 추가 정보
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(
        max_length=500, blank=True, help_text="자기소개를 500자 이내로 작성하세요.",
        validators=[MaxLengthValidator(500)]
    )

    class Meta:
        verbose_name = "사용자 프로필"
        verbose_name_plural = "사용자 프로필 목록"

    def __str__(self):
        return f"{self.user.nickname}의 프로필"


class EmailVerification(models.Model):
    """
    이메일 인증 모델
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at
