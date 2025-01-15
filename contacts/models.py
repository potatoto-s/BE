from django.core.validators import RegexValidator
from django.db import models


class Inquiry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r"^\d{2,3}-\d{3,4}-\d{4}$",
        message="전화번호는 '010-1234-5678' 형식으로 입력해주세요.",
    )
    phone = models.CharField(max_length=20, validators=[phone_regex], null=True, blank=True)
    content = models.TextField()
    preferred_contact = models.CharField(
        max_length=20,
        choices=[("EMAIL", "EMAIL"), ("PHONE", "PHONE")],
        help_text="선호하는 연락 방법을 선택해주세요.",
    )
    inquiry_type = models.CharField(
        max_length=20,
        choices=[("COMPANY", "COMPANY"), ("WORKSHOP", "WORKSHOP")],
        help_text="문의 유형을 선택해주세요.",
    )
    organization_name = models.CharField(
        max_length=255,
        help_text="문의할 기업명 또는 공방명을 입력해주세요.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"문의 {self.id} - {self.name}"

    class Meta:
        db_table = "inquiries"
        verbose_name = "문의"
        verbose_name_plural = "문의"
        ordering = ["-created_at"]
