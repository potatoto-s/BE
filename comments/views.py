from typing import Any

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.serializers import CommentCreateSerializer, CommentSerializer, CommentUpdateSerializer
from comments.services import CommentService


class CommentListView(APIView):
    # 댓글 목록 조회
    MIN_PAGE_SIZE: int = 1
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 50
    DEFAULT_PAGE: int = 1

    def validate_pagination_params(self, page: Any, limit: Any) -> tuple[int, int]:
        try:
            page = int(page) if page else self.DEFAULT_PAGE
            limit = int(limit) if limit else self.DEFAULT_PAGE_SIZE

            if page < self.MIN_PAGE_SIZE:
                raise ValidationError(f"Page number must be at least {self.MIN_PAGE_SIZE}.")

            if limit < self.MIN_PAGE_SIZE:
                raise ValidationError(f"Page size must be at least {self.MIN_PAGE_SIZE}.")
            if limit > self.MAX_PAGE_SIZE:
                raise ValidationError(f"Page size cannot exceed {self.MAX_PAGE_SIZE}.")

            return page, limit

        except ValueError:
            raise ValidationError("Invalid pagination parameters: must be numbers")

    def get(self, request: Request, post_id: int) -> Response:
        # 게시글 목록 조회
        page, limit = self.validate_pagination_params(
            request.query_params.get("page"),
            request.query_params.get("limit"),
        )
        offset = (page - 1) * limit

        # 댓글 목록 조회
        comments, total_count = CommentService.get_post_comments(
            post_id=post_id,
            offset=offset,
            limit=limit,
        )

        serializer = CommentSerializer(comments, many=True, context={"request": request})

        return Response(
            {
                "data": serializer.data,
                "pagination": {
                    "total_pages": (total_count + limit - 1) // limit,
                    "current_page": page,
                    "total_count": total_count,
                    "has_next": (page * limit) < total_count,
                    "has_previous": page > 1,
                    "limit": limit,
                },
            }
        )


class CommentCreateView(APIView):
    # 댓글 작성
    def post(self, request: Request, post_id: int) -> Response:
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 댓글 생성
        comment = CommentService.create_comment(
            post_id=post_id,
            user_id=request.user.id,
            data=serializer.validated_data,
        )

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class CommentUpdateView(APIView):
    # 댓글 수정

    def patch(self, request: Request, comment_id: int) -> Response:
        serializer = CommentUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 댓글 수정
        comment = CommentService.update_comment(
            comment_id=comment_id,
            user_id=request.user.id,
            data=serializer.validated_data,
        )

        return Response(CommentSerializer(comment).data)


class CommentDeleteView(APIView):
    # 댓글 삭제

    def delete(self, request: Request, comment_id: int) -> Response:
        CommentService.delete_comment(
            comment_id=comment_id,
            user_id=request.user.id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
