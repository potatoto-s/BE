from typing import Any, Dict, List, Optional, Tuple

from django.db import transaction
from django.db.models import F, Prefetch, Q, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from posts.models import Post, PostImage, PostLike


class PostService:
    @staticmethod
    def get_post_list(
        category: Optional[str] = None,
        search_keyword: Optional[str] = None,
        cursor: Optional[int] = None,
        limit: int = 10,
        is_top_liked: bool = False,
    ) -> Tuple[List[Post], bool, Optional[int]]:
        # 카테고리 검증
        category = PostService.validate_category(category)

        # 기본 쿼리셋 구성
        queryset = (
            Post.objects.select_related("user").prefetch_related("images").filter(is_deleted=False)
        )
        # 카테고리 limit 설정
        if limit not in [5, 10]:
            limit = 10

        # 좋아요 TOP 10 조회
        if is_top_liked:
            posts = list(queryset.order_by("-like_count", "-created_at")[:10])
            return posts, False, None

        # 기존 로직
        if category:
            queryset = queryset.filter(category=category)

        if search_keyword:
            queryset = queryset.filter(
                Q(title__icontains=search_keyword) | Q(content__icontains=search_keyword)
            )

        # 커서 기반 페이지네이션
        if cursor:
            queryset = queryset.filter(id__lt=cursor)

        # 정렬 및 제한
        posts = list(queryset.order_by("-id")[: limit + 1])
        posts_list = list(posts)

        # 다음 페이지 존재 여부 확인
        has_next = len(posts_list) > limit
        if has_next:
            posts_list = posts_list[:-1]
            next_cursor = posts_list[-1].id
        else:
            next_cursor = None

        return posts_list, has_next, next_cursor

    @staticmethod
    def get_user_posts(
        user_id: int, cursor: Optional[int] = None, limit: int = 10
    ) -> Tuple[List[Post], bool, Optional[int]]:
        queryset = (
            Post.objects.select_related("user")
            .prefetch_related("images", "comments")
            .filter(user_id=user_id, is_deleted=False)
        )

        if cursor:
            queryset = queryset.filter(id__lt=cursor)

        posts = queryset.order_by("-id")[: limit + 1]
        posts_list = list(posts)

        has_next = len(posts_list) > limit
        if has_next:
            posts_list = posts_list[:-1]
            next_cursor = posts_list[-1].id
        else:
            next_cursor = None

        return posts_list, has_next, next_cursor

    @staticmethod
    def get_post_detail(post_id: int, user_id: Optional[int] = None) -> Post:
        queryset = Post.objects.select_related("user").prefetch_related(
            "images",
            "comments__user",  # 댓글과 댓글 작성자 정보도 함께 조회
        )

        if user_id:
            likes_prefetch = Prefetch("likes", queryset=PostLike.objects.filter(user_id=user_id))
            queryset = queryset.prefetch_related(likes_prefetch)

        post = get_object_or_404(queryset, id=post_id, is_deleted=False)
        return post

    @staticmethod
    def increase_view_count(post_id: int) -> None:
        Post.objects.filter(id=post_id).update(view_count=F("view_count") + 1)

    @staticmethod
    @transaction.atomic
    def create_post(user_id: int, data: Dict[str, Any], images: Optional[List[Any]] = None) -> Post:
        post = Post.objects.create(
            user_id=user_id,
            title=data["title"],
            content=data["content"],
            category=data["category"],
        )

        if images:
            PostService._handle_images(post, images)

        return post

    @staticmethod
    @transaction.atomic
    def update_post(
        post_id: int,
        user_id: int,
        data: Dict[str, Any],
        add_image: Optional[List[Any]] = None,
        remove_image_ids: Optional[List[int]] = None,
    ) -> Post:
        post = get_object_or_404(Post, id=post_id, is_deleted=False)

        if post.user_id != user_id:
            raise PermissionDenied("자신의 게시글만 수정할 수 있습니다.")

        for key, value in data.items():
            setattr(post, key, value)
        post.save()

        if add_image:
            PostService._handle_images(post, add_image)

        if remove_image_ids:
            PostImage.objects.filter(
                post_id=post_id,
                id__in=remove_image_ids,
            ).delete()

        return post

    @staticmethod
    def delete_post(post_id: int, user_id: int) -> None:
        post = get_object_or_404(Post, id=post_id, is_deleted=False)

        if post.user_id != user_id:
            raise ValidationError("자신의 게시글만 삭제할 수 있습니다.")

        post.delete()

    @staticmethod
    def validate_category(category: Optional[str]) -> Optional[str]:
        if category and category not in dict(Post.Category.choices):
            raise ValidationError(f"Invalid category: {category}")
        return category

    @staticmethod
    def _handle_images(post: Post, images: List[str]) -> None:
        image_instances = [PostImage(post=post, image_url=image) for image in images]
        PostImage.objects.bulk_create(image_instances)

    @staticmethod
    @transaction.atomic
    def toggle_like(post_id: int, user_id: int) -> bool:
        post = get_object_or_404(Post.objects.select_for_update(), id=post_id, is_deleted=False)

        like, created = PostLike.objects.get_or_create(
            post_id=post_id,
            user_id=user_id,
        )

        if not created:
            like.delete()
            post.like_count = F("like_count") - 1
            post.save()
            post.refresh_from_db()
            return False

        post.like_count = F("like_count") + 1
        post.save()
        post.refresh_from_db()
        return True
