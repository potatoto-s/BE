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
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})

        role = attrs.get("role")
        if role == User.Role.COMPANY:
            if not attrs.get("company_name"):
                raise serializers.ValidationError(
                    {"company_name": "기업 회원은 기업명을 입력해야 합니다."}
                )
            attrs.pop("workshop_name", None)
        elif role == User.Role.WORKSHOP:
            if not attrs.get("workshop_name"):
                raise serializers.ValidationError(
                    {"workshop_name": "공방 회원은 공방명을 입력해야 합니다."}
                )
            attrs.pop("company_name", None)

        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data["user"] = {
            "id": user.id,
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
        fields = (
            "id",
            "email",
            "name",
            "nickname",
            "phone",
            "role",
            "company_name",
            "workshop_name",
        )
        read_only_fields = ("id", "email", "role")

    def validate(self, attrs):
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


class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용중인 이메일입니다.")
        return value


class CheckNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField()

    def validate_nickname(self, value):
        if User.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용중인 닉네임입니다.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password2"]:
            raise serializers.ValidationError({"new_password": "새 비밀번호가 일치하지 않습니다."})
        return attrs
