from typing import Any, Dict, List, Tuple

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from comments.models import Comment
from posts.models import Post


class CommentService:
    @staticmethod
    def get_post_comments(
        post_id: int,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[List[Comment], int]:

        # 게시글 존재 여부 확인
        get_object_or_404(Post, id=post_id, is_deleted=False)

        # 게시글 댓글 목록 조회
        queryset = (
            Comment.objects.select_related("user")
            .filter(post_id=post_id, is_deleted=False)
            .order_by("-created_at")
        )

        total_count = queryset.count()
        comments = list(queryset.order_by("-created_at")[offset : offset + limit])

        return comments, total_count

    @staticmethod
    @transaction.atomic
    def create_comment(
        post_id: int,
        user_id: int,
        data: Dict[str, Any],
    ) -> Comment:

        # 게시글과 작성자 정보를 한 번에 조회
        # 게시글 존재 여부 확인
        get_object_or_404(
            Post,
            id=post_id,
            is_deleted=False,
        )

        # 댓글 생성
        comment = Comment.objects.create(
            post_id=post_id,
            user_id=user_id,
            content=data["content"],
        )

        # 게시글의 댓글 수 증가
        Post.objects.filter(id=post_id).update(comment_count=F("comment_count") + 1)

        return comment

    @staticmethod
    @transaction.atomic
    def update_comment(
        comment_id: int,
        user_id: int,
        data: Dict[str, Any],
    ) -> Comment:

        comment = get_object_or_404(
            Comment.objects.select_related("post"),
            id=comment_id,
            is_deleted=False,
        )

        # 권한 체크
        if comment.user_id != user_id:
            raise ValidationError("자신의 댓글만 수정할 수 있습니다.")

        # 삭제된 게시글의 댓글인지 확인
        if comment.post.is_deleted:
            raise ValidationError("삭제된 게시글의 댓글은 수정할 수 없습니다.")

        # 댓글 수정
        comment.content = data["content"]
        comment.save()

        return comment

    @staticmethod
    @transaction.atomic
    def delete_comment(comment_id: int, user_id: int) -> None:
        # select_for_update로 동시성 제어
        comment = get_object_or_404(
            Comment.objects.select_for_update(), id=comment_id, is_delete=False
        )

        if comment.user_id != user_id:
            raise ValidationError("자신의 댓글만 삭제할 수 있습니다.")

        Post.objects.filter(id=comment.post_id).update(
            comment_count=F("comment_count") - 1
        )

        # 커스텀 delete 메서드 호출
        comment.delete()

    @classmethod
    def _validate_post(cls, post_id: int) -> None:
        # 게시글 유효성 검증
        get_object_or_404(Post, id=post_id, is_deleted=False)

    @classmethod
    def _validate_comment_owner(cls, comment: Comment, user_id: int) -> None:
        # 댓글 작성자 검증
        if comment.user_id != user_id:
            raise ValidationError("자신의 댓글만 수정/삭제할 수 있습니다.")
