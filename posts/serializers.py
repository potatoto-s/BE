from typing import Any, Dict

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from comments.serializers import CommentResponseSerializer

# from rest_framework.exceptions import ValidationError
from posts.models import Post, PostImage, PostLike

User = get_user_model()


class BaseSerializer(serializers.Serializer[Any]):
    class Meta:
        abstract = True


class PostImageSerializer(BaseSerializer):
    # 게시글 이미지 시리얼라이저

    id = serializers.IntegerField(read_only=True)
    image_url = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data: Dict[str, Any]) -> PostImage:
        return PostImage.objects.create(**validated_data)


class PostCreateSerializer(BaseSerializer):
    # 공방 사장만 게시글 작성 가능
    # 제목, 내용, 카테고리 필수 입력

    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    category = serializers.ChoiceField(choices=Post.Category.choices)
    images = serializers.ListField(child=serializers.ImageField(), required=False, write_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = self.context["request"].user
        if not user.is_authenticated:
            raise ValidationError("로그인이 필요합니다.")

        # TODO: User 모델 구현 후 수정 필요
        # User 모델에 실제로 있어야함 ['role']
        if getattr(user, "role", None) != "WORKSHOP":
            raise ValidationError("공방 회원만 게시글을 작성할 수 있습니다.")
        return attrs

    def create(self, validated_data: Dict[str, Any]) -> Post:
        # 이미지는 별도 PostImage 모델에 저장
        # 생성자 정보는 request.user에서 자동으로 설정
        images = validated_data.pop("images", [])
        validated_data["user"] = self.context["request"].user
        post = Post.objects.create(**validated_data)

        # 이미지 처리 = service layer에서 구현
        return post


class PostListSerializer(BaseSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(read_only=True)

    def get_author(self, obj: Post) -> Dict[str, Any]:
        # 작성자 정보를 딕셔너리로 반환
        return {
            "id": obj.user.id,
            # TODO: User 모델 구현 후 수정 필요
            # User 모델에 실제로 있어야함 ['nickname']
            "nickname": getattr(obj.user, "nickname", ""),
            # TODO: User 모델 구현 후 수정 필요
            # User 모델에 실제로 있어야함 ['workshop_name']
            "workshop_name": getattr(obj.user, "workshop_name", ""),
        }


class PostDetailSerializer(BaseSerializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)
    category = serializers.CharField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    author = serializers.SerializerMethodField()
    images = PostImageSerializer(many=True, read_only=True)
    is_liked = serializers.SerializerMethodField()
    comments = CommentResponseSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_author(self, obj: Post) -> Dict[str, Any]:
        # 작성자 정보를 딕셔너리로 반환
        return {
            "id": obj.user.id,
            # TODO: User 모델 구현 후 수정 필요
            # User 모델에 실제로 있어야함 ['nickname']
            "nickname": getattr(obj.user, "nickname", ""),
            # TODO: User 모델 구현 후 수정 필요
            # User 모델에 실제로 있어야함 ['workshop_name']
            "workshop_name": getattr(obj.user, "workshop_name", ""),
        }

    def get_is_liked(self, obj: Post) -> bool:
        # 현재 사용자의 게시글 좋아요 여부 확인
        user = self.context["request"].user
        if user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False


class PostUpdateSerializer(BaseSerializer):
    # 자신의 게시글만 수정 가능
    # 수정할 필드는 선택적으로 입력 가능
    title = serializers.CharField(max_length=255, required=False)
    content = serializers.CharField(required=False)
    category = serializers.ChoiceField(choices=Post.Category.choices, required=False)
    add_images = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )
    remove_image_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, write_only=True
    )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        # 수정 권한 검증
        # self.instance가 None이 아닌지 확인
        if self.instance is not None and self.instance.user != self.context["request"].user:
            raise ValidationError("자신의 게시글만 수정할 수 있습니다.")
        return attrs

    def update(self, instance: Post, validated_data: Dict[str, Any]) -> Post:
        # 게시글 수정
        # 입력된 필드만 선택적으로 수정
        # 삭제된 게시글 수정 방지

        if instance.is_deleted:
            raise ValidationError("삭제된 게시글은 수정할 수 없습니다.")

        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.category = validated_data.get("category", instance.category)
        instance.save()

        # 수정된 게시글 인스턴스
        return instance


# User 모델 role 필드 확인
# WORKSHOP 값이 유효한지 확인
# User 모델에 nickname 필드 확인
# User 모델에 workshop_name 확인


# User 모델 스키마를 공유하고 필드명을 맞추기
# User 모델의 role 상수값 (예: "WORKSHOP")을 공유하거나 enum으로 정의
# 필요한 경우 User 타입에 대한 타입 힌트도 공유
