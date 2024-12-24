from typing import Any, Optional, Type

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager["User"]):
    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "User":
        if not email:
            raise ValueError("이메일은 필수 값입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "WORKSHOP")  # WORKSHOP으로 수정
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        COMPANY = "COMPANY", "기업"
        WORKSHOP = "WORKSHOP", "공방"

    # AbstractUser의 기본 필드 중 사용하지 않을 필드 무효화
    username: None = None  # type: ignore
    first_name: None = None  # type: ignore
    last_name: None = None  # type: ignore

    # 기존 필드 재정의 및 새로운 필드 추가
    email = models.EmailField(
        "이메일",
        max_length=255,
        unique=True,
        error_messages={
            "unique": "이미 사용중인 이메일입니다.",
        },
    )
    name = models.CharField(
        "이름", max_length=100, help_text="사용자의 실명을 입력해주세요."
    )
    nickname = models.CharField(
        "닉네임",
        max_length=100,
        unique=True,
        error_messages={
            "unique": "이미 사용중인 닉네임입니다.",
        },
    )
    phone_regex = RegexValidator(
        regex=r"^\d{10,11}$", message="전화번호는 10~11자리의 숫자로만 입력해주세요."
    )
    phone = models.CharField(
        "전화번호",
        max_length=20,
        validators=[phone_regex],
        help_text="'-' 없이 숫자만 입력해주세요.",
    )
    role = models.CharField(
        "역할",
        max_length=20,
        choices=Role.choices,
        help_text="기업 또는 공방을 선택해주세요.",
    )
    company_name = models.CharField(
        "기업명",
        max_length=255,
        blank=True,
        null=True,
        help_text="기업 회원의 경우 필수 입력사항입니다.",
    )
    workshop_name = models.CharField(
        "공방명",
        max_length=255,
        blank=True,
        null=True,
        help_text="공방 회원의 경우 필수 입력사항입니다.",
    )
    created_at = models.DateTimeField("가입일", default=timezone.now, editable=False)
    updated_at = models.DateTimeField("정보 수정일", auto_now=True)

    objects = UserManager()  # type: ignore

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "nickname", "phone", "role"]

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.email} ({self.nickname})"

    def save(self, *args: Any, **kwargs: Any) -> None:
        if self.role == self.Role.COMPANY and not self.company_name:
            raise ValueError("기업 회원은 기업명을 입력해야 합니다.")
        if self.role == self.Role.WORKSHOP and not self.workshop_name:
            raise ValueError("공방 회원은 공방명을 입력해야 합니다.")
        super().save(*args, **kwargs)
