from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 값입니다.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "COMPANY")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        COMPANY = "COMPANY", "기업"
        WORKSHOP = "WORKSHOP", "공방"

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(
        "이메일",
        max_length=255,
        unique=True,
        error_messages={
            "unique": "이미 사용중인 이메일입니다.",
        },
    )
    name = models.CharField("이름", max_length=100, help_text="사용자의 실명을 입력해주세요.")
    nickname = models.CharField(
        "닉네임",
        max_length=100,
        unique=True,
        error_messages={
            "unique": "이미 사용중인 닉네임입니다.",
        },
    )
    phone_regex = RegexValidator(
        regex=r"^\d{2,3}-\d{3,4}-\d{4}$",
        message="전화번호는 '010-1234-5678' 형식으로 입력해주세요.",
    )
    phone = models.CharField(
        "전화번호",
        max_length=20,
        validators=[phone_regex],
        help_text="'-'를 포함하여 입력해주세요. (예: 010-1234-5678)",
    )
    role = models.CharField(
        "역할", max_length=20, choices=Role.choices, help_text="기업 또는 공방을 선택해주세요."
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

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "nickname", "phone", "role"]

    class Meta:
        db_table = "users"
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} ({self.nickname})"

    def save(self, *args, **kwargs):
        if self.role == self.Role.COMPANY and not self.company_name:
            raise ValueError("기업 회원은 기업명을 입력해야 합니다.")
        if self.role == self.Role.WORKSHOP and not self.workshop_name:
            raise ValueError("공방 회원은 공방명을 입력해야 합니다.")
        super().save(*args, **kwargs)
