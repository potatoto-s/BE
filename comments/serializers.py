from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from comments.models import Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer[Any]):
    class Meta:
        model = Comment
        fields = "__all__"


class BaseSerializer(serializers.Serializer[Any]):
    class Meta:
        abstract = True


class CommentCreateSerializer(BaseSerializer):
    # 댓글 생성 시리얼라이저
    # 회원(기업 공방)만 작성 가능
    # 댓글 내용 필수 입력
    content = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context["request"].user
        if not user.is_authenticated:
            raise ValidationError("로그인이 필요합니다.")

        # TODO: User 모델 구현 후 수정 필요
        if getattr(user, "role", None) not in ["COMPANY", "WORKSHOP"]:
            raise ValidationError("기업회원과 공방회원만 댓글을 작성할 수 있습니다.")

        # 삭제된 게시글에는 댓글을 작성할 수 없음
        post = self.context.get("post")
        if not post:
            raise ValidationError("게시글 정보가 제공되지 않았습니다.")
        if post.is_deleted:
            raise ValidationError("삭제된 게시글에는 댓글을 작성할 수 없습니다.")

        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Comment:
        validated_data["user"] = self.context["request"].user
        validated_data["post_id"] = self.context["post_id"]
        comment = Comment.objects.create(**validated_data)
        return comment


class CommentResponseSerializer(BaseSerializer):
    # 댓글 시리얼라이저
    # 작성자 정보 포함 (기업명 표시 / 공방명 표시)
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(read_only=True)
    author = serializers.SerializerMethodField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_author(self, obj: Comment) -> Dict[str, Any]:
        user = obj.user
        role = getattr(user, "role", "")
        result = {
            "id": user.id,
            "role": role,
        }

        # 기업회원 - 기업명 / 공방회원 - 공방명 표시
        if role == "COMPANY":
            # TODO: User 모델 구현 후 수정 필요
            # User 모델에 실제로 있어야함 ['company_name']
            result["company_name"] = getattr(user, "company_name", "")

        elif role == "WORKSHOP":
            # TODO: User 모델 구현 후 수정 필요
            # User 모델에 실제로 있어야함 ['company_name']
            result["workshop_name"] = getattr(user, "workshop_name", "")

        return result

    def to_representation(self, instance: Comment) -> Dict[str, Any]:
        # 삭제된 댓글인 경우 content를 '삭제된 댓글입니다.' 로 표시
        data = super().to_representation(instance)
        if instance.is_deleted:
            data["content"] = "삭제된 댓글입니다."
        return data


class CommentUpdateSerializer(BaseSerializer):
    # 댓글 수정 시리얼라이저
    # 자신이 작성한 댓글만 수정 가능
    # 내용만 수정 가능
    content = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        # 댓글 존재 여부 확인
        if not self.instance:
            raise ValidationError("수정할 댓글이 존재하지 않습니다.")

        # 권한 및 상태 검증
        if self.instance.user != self.context["request"].user:
            raise ValidationError("자신의 댓글만 수정할 수 있습니다.")
        if self.instance.is_deleted:
            raise ValidationError("삭제된 댓글은 수정할 수 없습니다.")
        if self.instance.post.is_deleted:
            raise ValidationError("삭제된 게시글의 댓글은 수정할 수 없습니다.")

        return attrs

    def update(self, instance: Comment, validated_data: Dict[str, Any]) -> Comment:
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


# User 모델 role 필드 존재 여부
# "COMPANY", "WORKSHOP" 값 유효성 체크
# User 모델 company_name, workshop_name 필드 존재 여부
