from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Inquiry


class InquirySerializer(serializers.ModelSerializer):
    phone_regex = RegexValidator(
        regex=r"^\d{2,3}-\d{3,4}-\d{4}$",
        message="전화번호는 '010-1234-5678' 형식으로 입력해주세요.",
    )

    email = serializers.EmailField(required=False, allow_null=True)
    phone = serializers.CharField(required=False, allow_null=True, validators=[phone_regex])
    organization_name = serializers.CharField(
        error_messages={
            "required": "문의 유형이 COMPANY인 경우 기업명을, WORKSHOP인 경우 공방명을 입력해주세요.",
            "blank": "문의 유형이 COMPANY인 경우 기업명을, WORKSHOP인 경우 공방명을 입력해주세요.",
        }
    )

    class Meta:
        model = Inquiry
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "content",
            "organization_name",
            "preferred_contact",
            "inquiry_type",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        # 문의 유형에 따른 organization_name 검증
        inquiry_type = data.get("inquiry_type")
        organization_name = data.get("organization_name")

        if inquiry_type == "COMPANY":
            if not organization_name:
                raise serializers.ValidationError(
                    {"organization_name": "기업 문의 시 기업명은 필수입니다."}
                )
        elif inquiry_type == "WORKSHOP":
            if not organization_name:
                raise serializers.ValidationError(
                    {"organization_name": "공방 문의 시 공방명은 필수입니다."}
                )

        # preferred_contact에 따른 연락처 검증
        preferred_contact = data.get("preferred_contact")
        email = data.get("email")
        phone = data.get("phone")

        if preferred_contact == "EMAIL":
            if not email:
                raise serializers.ValidationError(
                    {"email": "이메일 연락 방식을 선택하셨으므로 이메일은 필수입니다."}
                )
            # 이메일 형식 추가 검증
            if not email or not "@" in email:
                raise serializers.ValidationError(
                    {"email": "이메일은 'example@example.com' 형식으로 입력해주세요."}
                )
        elif preferred_contact == "PHONE":
            if not phone:
                raise serializers.ValidationError(
                    {"phone": "전화 연락 방식을 선택하셨으므로 전화번호는 필수입니다."}
                )
            # 전화번호 형식 추가 검증
            if not phone or not "-" in phone:
                raise serializers.ValidationError(
                    {"phone": "전화번호는 '010-1234-5678' 형식으로 입력해주세요."}
                )

        return data

    def to_internal_value(self, data):
        # email과 phone을 선택적으로 만듦
        if "email" not in data:
            data["email"] = None
        if "phone" not in data:
            data["phone"] = None
        return super().to_internal_value(data)
