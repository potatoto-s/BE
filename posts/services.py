from typing import Any, Dict, List, Optional, Tuple

from django.db import transaction
from django.db.models import F, Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied, ValidationError

from posts.models import Post, PostImage, PostLike


class PostService:
    # 게시글 비즈니스 로직

    @staticmethod
    # category: 필터링 할 카테고리
    # search_keyword: 검색어(제목, 내용)
    # offset: 시작 위치
    # limit: 조회할 게시글 수
    def get_post_list(
        category: Optional[str] = None,
        search_keyword: Optional[str] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[Post], int]:
        # 게시글 목록 조회 (with 필터링, 검색)

        # 카테고리 검증
        category = PostService.validate_category(category)

        # 기본 쿼리셋 구성
        queryset = (
            Post.objects.select_related("user")
            .prefetch_related("images")
            .filter(is_deleted=False)
        )

        if category:
            queryset = queryset.filter(category=category)

        if search_keyword:
            queryset = queryset.filter(
                Q(title__icontains=search_keyword)
                | Q(content__icontains=search_keyword)
            )

        total_count = queryset.count()
        posts = queryset.order_by("-created_at")[offset : offset + limit]

        return list(posts), total_count

    @staticmethod
    def get_post_detail(post_id: int, user_id: Optional[int] = None) -> Post:
        # 게시글 상세 조회
        # 조회수 증가

        # 기본 쿼리셋 구성
        queryset = Post.objects.select_related("user").prefetch_related("images")

        # 로그인한 사용자의 경우에만 좋아요 정보 prefetch
        if user_id:
            likes_prefetch = Prefetch(
                "likes", queryset=PostLike.objects.filter(user_id=user_id)
            )
            queryset = queryset.prefetch_related(likes_prefetch)

        post = get_object_or_404(queryset, id=post_id, is_deleted=False)

        # 조회수 증가 (race condition 방지를 위해 F 표현식 사용)
        Post.objects.filter(id=post_id).update(view_count=F("view_count") + 1)

        return post

    @staticmethod
    @transaction.atomic
    def create_post(
        user_id: int, data: Dict[str, Any], images: Optional[List[Any]] = None
    ) -> Post:
        # 게시글 생성
        post = Post.objects.create(
            user_id=user_id,
            title=data["title"],
            content=data["content"],
            category=data["category"],
        )

        # 이미지 처리
        if images:
            PostService._handle_images(post, images)

        return post

    @staticmethod
    @transaction.atomic
    def update_post(
        # 게시글 수정
        post_id: int,
        user_id: int,
        data: Dict[str, Any],
        add_image: Optional[List[Any]] = None,
        remove_image_ids: Optional[List[int]] = None,
    ) -> Post:

        post = get_object_or_404(Post, id=post_id, is_deleted=False)

        # 권한 확인
        if post.user_id != user_id:
            raise PermissionDenied("자신의 게시글만 수정할 수 있습니다.")

        # 기본 정보 수정
        for key, value in data.items():
            setattr(post, key, value)
        post.save()

        # 이미지 추가
        if add_image:
            PostService._handle_images(post, add_image)

        # 이미지 삭제
        if remove_image_ids:
            PostImage.objects.filter(
                post_id=post_id,
                id__in=remove_image_ids,
            ).delete()

        return post

    @staticmethod
    def delete_post(post_id: int, user_id: int) -> None:
        # 게시글 삭제 (소프트 딜리트)

        post = get_object_or_404(Post, id=post_id, is_deleted=False)

        # 권한 체크
        if post.user_id != user_id:
            raise ValidationError("자신의 게시글만 삭제할 수 있습니다.")

        # 모델의 커스텀 delete 메서드 호출 (소프트 딜리트))
        post.delete()

    @staticmethod
    def validate_category(category: Optional[str]) -> Optional[str]:
        if category and category not in dict(Post.Category.choices):
            raise ValidationError(f"Invalid category: {category}")
        return category

    @staticmethod
    def _handle_images(post: Post, images: List[str]) -> None:
        # 이미지 처리 헬퍼 메서드
        image_instances = [PostImage(post=post, image_url=image) for image in images]

        PostImage.objects.bulk_create(image_instances)

    @staticmethod
    @transaction.atomic
    def toggle_like(post_id: int, user_id: int) -> bool:
        # 좋아요 토글

        post = get_object_or_404(
            Post.objects.select_for_update(), id=post_id, is_deleted=False
        )

        like, created = PostLike.objects.get_or_create(
            post_id=post_id,
            user_id=user_id,
        )

        # 좋아요 수 업데이트
        if not created:
            like.delete()
            post.like_count = F("like_count") - 1
            post.save()
            post.refresh_from_db()  # F 표현식 사용 후 값 갱신
            return False

        post.like_count = F("like_count") + 1
        post.save()
        post.refresh_from_db()  # F 표현식 사용 후 값 갱신
        return True
