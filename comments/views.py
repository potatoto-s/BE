from typing import Any

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import authentication, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from comments.models import Comment
from comments.permissions import IsAuthenticatedWithUnauthorized
from comments.serializers import CommentCreateSerializer, CommentSerializer, CommentUpdateSerializer
from comments.services import CommentService
from posts.models import Post


class CommentListView(APIView):
    authentication_classes = [JWTAuthentication]  # TokenAuthentication에서 변경
    permission_classes = [IsAuthenticatedWithUnauthorized]
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

    @extend_schema(
        parameters=[
            OpenApiParameter(name="page", type=int, description="Page number"),
            OpenApiParameter(name="limit", type=int, description="Items per page"),
        ],
        responses={200: CommentSerializer(many=True)},
    )
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
    serializer_class = CommentCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedWithUnauthorized]

    @extend_schema(request=CommentCreateSerializer, responses={201: CommentSerializer})
    # 댓글 작성
    def post(self, request: Request, post_id: int) -> Response:
        # post 존재 여부 확인
        post = get_object_or_404(Post, id=post_id, is_deleted=False)

        serializer = CommentCreateSerializer(
            data=request.data, context={"request": request, "post": post}
        )
        serializer.is_valid(raise_exception=True)

        comment = CommentService.create_comment(
            post_id=post_id,
            user_id=request.user.id,
            data=serializer.validated_data,
        )

        return Response(
            CommentSerializer(comment, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class CommentUpdateView(APIView):
    serializer_class = CommentUpdateSerializer
    authentication_classes = [JWTAuthentication]

    @extend_schema(request=CommentUpdateSerializer, responses={200: CommentSerializer})
    # 댓글 수정
    def patch(self, request: Request, comment_id: int) -> Response:
        comment = get_object_or_404(Comment, id=comment_id, is_deleted=False)

        serializer = CommentUpdateSerializer(
            comment, data=request.data, context={"request": request}  # instance 추가
        )
        serializer.is_valid(raise_exception=True)

        # 댓글 수정
        updated_comment = CommentService.update_comment(
            comment_id=comment_id,
            user_id=request.user.id,
            data=serializer.validated_data,
        )

        return Response(CommentSerializer(updated_comment, context={"request": request}).data)


class CommentDeleteView(APIView):
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication]

    @extend_schema(responses={204: None})
    # 댓글 삭제
    def delete(self, request: Request, comment_id: int) -> Response:
        CommentService.delete_comment(
            comment_id=comment_id,
            user_id=request.user.id,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
