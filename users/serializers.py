from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "name",
            "nickname",
            "phone",
            "role",
            "company_name",
            "workshop_name",
        )
        extra_kwargs = {"company_name": {"required": False}, "workshop_name": {"required": False}}

    def validate(self, attrs):
        # 비밀번호 일치 검증
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        # role에 따른 필수 필드 검증
        role = attrs.get("role")
        if role == User.Role.COMPANY:
            if not attrs.get("company_name"):
                raise serializers.ValidationError(
                    {"company_name": "기업 회원은 기업명을 입력해야 합니다."}
                )
            # 공방명이 입력된 경우 제거
            attrs.pop("workshop_name", None)
        elif role == User.Role.WORKSHOP:
            if not attrs.get("workshop_name"):
                raise serializers.ValidationError(
                    {"workshop_name": "공방 회원은 공방명을 입력해야 합니다."}
                )
            # 기업명이 입력된 경우 제거
            attrs.pop("company_name", None)

        return attrs

    def create(self, validated_data):
        # password2 필드 제거
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # 기본 검증 및 토큰 생성
        data = super().validate(attrs)

        # 응답에 사용자 정보 추가
        user = self.user
        data["user"] = {
            "email": user.email,
            "name": user.name,
            "nickname": user.nickname,
            "phone": user.phone,
            "role": user.role,
            "company_name": user.company_name,
            "workshop_name": user.workshop_name,
        }

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name", "nickname", "phone", "role", "company_name", "workshop_name")
        read_only_fields = ("email", "role")  # 이메일과 역할은 수정 불가
        extra_kwargs = {"company_name": {"required": False}, "workshop_name": {"required": False}}

    def validate(self, attrs):
        # role에 따른 필드 검증
        user = self.context["request"].user
        if user.role == User.Role.COMPANY:
            if attrs.get("workshop_name"):
                raise serializers.ValidationError(
                    {"workshop_name": "기업 회원은 공방명을 설정할 수 없습니다."}
                )
        elif user.role == User.Role.WORKSHOP:
            if attrs.get("company_name"):
                raise serializers.ValidationError(
                    {"company_name": "공방 회원은 기업명을 설정할 수 없습니다."}
                )

        return attrs
