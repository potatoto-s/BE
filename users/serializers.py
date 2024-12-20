from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    district = serializers.CharField(required=True)
    neighborhood = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    workshop_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "confirm_password",
            "nickname",
            "district",
            "neighborhood",
            "role",
            "company_name",
            "workshop_name",
        )

    def validate(self, data):
        # 비밀번호 확인 검증
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        # 닉네임 길이 검증 (2~10자)
        if len(data["nickname"]) < 2 or len(data["nickname"]) > 10:
            raise serializers.ValidationError({"nickname": "닉네임은 2~10자 사이여야 합니다."})

        # 기업/공방 정보 검증
        if data["role"] == "company" and not data.get("company_name"):
            raise serializers.ValidationError({"company_name": "기업명은 필수 입력 항목입니다."})
        if data["role"] == "workshop" and not data.get("workshop_name"):
            raise serializers.ValidationError({"workshop_name": "공방명은 필수 입력 항목입니다."})

        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            username=validated_data["email"],
            **validated_data
        )
        UserProfile.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 시리얼라이저"""

    class Meta:
        model = UserProfile
        fields = ("bio",)


class UserDetailSerializer(serializers.ModelSerializer):
    """사용자 상세정보 시리얼라이저"""
    profilePhoto = serializers.ImageField(source='profile_image', required=False)
    bio = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(read_only=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    workshop_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = (
            'email',
            'nickname',
            'profilePhoto',
            'district',
            'neighborhood',
            'bio',
            'role',
            'company_name',
            'workshop_name',
        )
        read_only_fields = ('email', 'role')

    def to_representation(self, instance):
        """API 응답 형식에 맞게 데이터 변환"""
        ret = super().to_representation(instance)
        if hasattr(instance, 'profile') and instance.profile:
            ret['bio'] = instance.profile.bio
        return ret


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경 시리얼라이저"""
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({
                "new_password": "새 비밀번호가 일치하지 않습니다."
            })

        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({
                "new_password": e.messages
            })

        return data


class PasswordResetSerializer(serializers.Serializer):
    """비밀번호 재설정 시리얼라이저"""
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("등록되지 않은 이메일입니다.")
        return value


class EmailVerificationSerializer(serializers.Serializer):
    """이메일 인증 시리얼라이저"""
    user_id = serializers.IntegerField(required=True)
    code = serializers.CharField(required=True)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """커스텀 토큰 시리얼라이저"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserDetailSerializer(self.user).data
        return data
