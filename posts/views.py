from typing import Any, List

from django.db import transaction
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from PIL import Image
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import PostImage
from posts.serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostLikeResponseSerializer,
    PostListSerializer,
    PostSerializer,
    PostUpdateSerializer,
)
from posts.services import PostService


# 게시글 목록 조회
class PostListView(APIView):
    serializer_class = PostLikeResponseSerializer
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="cursor", type=int, description="마지막으로 본 게시글 ID"),
            OpenApiParameter(name="category", type=str, description="게시글 카테고리"),
            OpenApiParameter(name="search", type=str, description="검색어"),
            OpenApiParameter(name="top_liked", type=bool, description="좋아요 TOP 10 조회"),
            OpenApiParameter(name="limit", type=int, description="조회할 게시글 수 (5 또는 10)"),
        ],
        responses={200: PostListSerializer(many=True)},
    )
    def get(self, request: Request) -> Response:
        cursor_param = request.query_params.get("cursor")
        category = request.query_params.get("category")
        search = request.query_params.get("search")
        is_top_liked = request.query_params.get("top_liked") == "true"

        # 카테고리 limit 설정
        try:
            limit = int(request.query_params.get("limit", "10"))
            if limit not in [5, 10]:
                limit = 10
        except (ValueError, TypeError):
            limit = 10

        # cursor 파라미터 처리
        cursor = int(cursor_param) if cursor_param and cursor_param.isdigit() else None

        # context 구성
        context = {
            "user_id": request.user.id if request.user.is_authenticated else None,
            "request": request,
        }

        # 게시글 목록 조회
        posts, has_next, next_cursor = PostService.get_post_list(
            category=category,
            search_keyword=search,
            cursor=cursor,
            limit=limit,  # PAGE_SIZE 대신 limit 사용
            is_top_liked=is_top_liked,
        )

        serializer = PostListSerializer(posts, many=True, context=context)

        # TOP 10 조회 시에는 페이지네이션 정보 제외
        if is_top_liked:
            return Response({"data": serializer.data})

        return Response({"data": serializer.data, "has_next": has_next, "next_cursor": next_cursor})


class PostDetailView(APIView):
    serializer_class = PostDetailSerializer

    @extend_schema(responses={200: PostDetailSerializer})
    def get(self, request: Request, post_id: int) -> Response:
        post = PostService.get_post_detail(
            post_id=post_id,
            user_id=request.user.id if request.user.is_authenticated else None,
        )

        # 조회수 증가
        PostService.increase_view_count(post_id)

        context = {
            "request": request,
            "user_id": request.user.id if request.user.is_authenticated else None,
        }

        serializer = PostDetailSerializer(post, context=context)
        response = Response(serializer.data)
        response["Cache-Control"] = "max-age=60"
        return response


class PostCreateView(APIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # 로그인 사용자만 작성 가능

    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: set[str] = {"image/jpeg", "image/png", "image/gif"}
    MAX_IMAGE_COUNT: int = 10

    @classmethod
    def validate_images(cls, files: List[Any]) -> List[Any]:
        if not files:
            return files

        if len(files) > cls.MAX_IMAGE_COUNT:
            raise ValidationError(f"이미지는 최대 {cls.MAX_IMAGE_COUNT}개까지 업로드 가능합니다")

        total_size = 0
        for image in files:
            if not hasattr(image, "size"):
                raise ValidationError("올바르지 않은 이미지 파일입니다")

            total_size += image.size
            if image.size > cls.MAX_IMAGE_SIZE:
                raise ValidationError(
                    f"이미지 크기는 {cls.MAX_IMAGE_SIZE // 1024 // 1024}MB를 초과할 수 없습니다"
                )

            if (
                not hasattr(image, "content_type")
                or image.content_type not in cls.ALLOWED_IMAGE_TYPES
            ):
                raise ValidationError(f"허용된 이미지 형식: {', '.join(cls.ALLOWED_IMAGE_TYPES)}")

            try:
                Image.open(image).verify()
            except Exception:
                raise ValidationError("손상된 이미지 파일입니다")

        return files

    @extend_schema(request=PostCreateSerializer, responses={201: PostDetailSerializer})
    def post(self, request: Request) -> Response:
        serializer = PostCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        post = PostService.create_post(
            user_id=request.user.id,
            data=serializer.validated_data,
            images=request.FILES.getlist("images"),
        )

        return Response(
            PostDetailSerializer(post, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


class PostUpdateView(APIView):
    serializer_class = PostUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def validate_image_operations(
        self, post_id: int, add_images: List[Any], remove_image_ids: List[int]
    ) -> None:
        if remove_image_ids:
            existing_images = set(
                PostImage.objects.filter(post_id=post_id, id__in=remove_image_ids).values_list(
                    "id", flat=True
                )
            )
            invalid_ids = set(remove_image_ids) - existing_images
            if invalid_ids:
                raise ValidationError(f"존재하지 않는 이미지 ID: {invalid_ids}")

    @extend_schema(request=PostUpdateSerializer, responses={200: PostDetailSerializer})
    def patch(self, request: Request, post_id: int) -> Response:
        # 기존 request.data를 새로운 딕셔너리로 복사
        data = request.data.copy()

        # remove_image_ids 처리
        remove_ids = request.data.get("remove_image_ids", "")
        if isinstance(remove_ids, str) and remove_ids:
            try:
                remove_image_ids = [int(id_.strip()) for id_ in remove_ids.split(",")]
                data["remove_image_ids"] = remove_image_ids
            except ValueError:
                raise ValidationError("remove_image_ids must be valid integer IDs")

        serializer = PostUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        add_images = request.FILES.getlist("add_images")
        self.validate_image_operations(post_id, add_images, data.get("remove_image_ids", []))
        validated_images = PostCreateView.validate_images(add_images)

        post = PostService.update_post(
            post_id=post_id,
            user_id=request.user.id,
            data=serializer.validated_data,
            add_image=validated_images,
            remove_image_ids=data.get("remove_image_ids", []),
        )

        return Response(PostDetailSerializer(post, context={"request": request}).data)


class PostDeleteView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(responses={204: None})
    def delete(self, request: Request, post_id: int) -> Response:
        PostService.delete_post(post_id=post_id, user_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):
    serializer_class = PostLikeResponseSerializer

    @extend_schema(responses={200: PostLikeResponseSerializer})
    def post(self, request: Request, post_id: int) -> Response:
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인이 필요한 서비스입니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        is_liked = PostService.toggle_like(
            post_id=post_id,
            user_id=request.user.id,
        )
        return Response({"is_liked": is_liked, "message": "좋아요가 처리되었습니다"})


class UserPostListView(APIView):
    """사용자의 게시글 목록 조회 (마이페이지)"""

    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @extend_schema(
        parameters=[
            OpenApiParameter(name="cursor", type=int, description="마지막으로 본 게시글 ID"),
        ],
        responses={200: PostListSerializer(many=True)},
    )
    def get(self, request: Request) -> Response:
        if not request.user.is_authenticated:
            return Response(
                {"detail": "로그인이 필요한 서비스입니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        cursor_param = request.query_params.get("cursor")
        cursor = int(cursor_param) if cursor_param and cursor_param.isdigit() else None

        posts, has_next, next_cursor = PostService.get_user_posts(
            user_id=request.user.id, cursor=cursor, limit=10
        )

        serializer = PostListSerializer(posts, many=True, context={"request": request})
        return Response({"data": serializer.data, "has_next": has_next, "next_cursor": next_cursor})
