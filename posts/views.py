from typing import Any, List

from django.db import transaction
from PIL import Image
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import PostImage
from posts.serializers import (
    PostCreateSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostUpdateSerializer,
)
from posts.services import PostService


# 게시글 목록 조회
class PostListView(APIView):
    # 클래스 변수로 상수 정의
    MIN_PAGE_SIZE: int = 1
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 50
    DEFAULT_PAGE: int = 1

    def validate_pagination_params(self, page: Any, limit: Any) -> tuple[int, int]:
        # 페이지네이션 파라미터 검증
        try:
            page = int(page) if page else self.DEFAULT_PAGE
            limit = int(limit) if limit else self.DEFAULT_PAGE_SIZE

            if page < self.MIN_PAGE_SIZE:
                raise ValidationError(
                    f"Page number must be at least {self.MIN_PAGE_SIZE}"
                )

            if limit < self.MIN_PAGE_SIZE:
                raise ValidationError(
                    f"Page size must be at least {self.MIN_PAGE_SIZE}"
                )
            if limit > self.MAX_PAGE_SIZE:
                raise ValidationError(f"Page size cannot exceed {self.MAX_PAGE_SIZE}")

            return page, limit

        except ValueError:
            raise ValidationError("Invalid pagination parameters: must be numbers")

    def get(self, request: Request) -> Response:
        # 페이지네이션 파라미터 검증
        page, limit = self.validate_pagination_params(
            request.query_params.get("page"), request.query_params.get("limit")
        )
        offset = (page - 1) * limit

        category = request.query_params.get("category")
        search = request.query_params.get("search")

        # 캐시 키 생성
        cache_key = f"posts:list:{page}:{limit}"
        if category:
            cache_key += f":{category}"
        if search:
            cache_key += f":{search}"

        # context 구성
        context = {
            "user_id": request.user.id if request.user.is_authenticated else None,
            "request": request,
        }

        # 게시글 목록 조회
        posts, total_count = PostService.get_post_list(
            category=category,
            search_keyword=search,
            offset=offset,
            limit=limit,
        )

        # 데이터 직렬화
        serializer = PostListSerializer(posts, many=True, context=context)

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


class PostCreateView(APIView):
    MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5MB
    ALLOWED_IMAGE_TYPES: set[str] = {"image/jpeg", "image/png", "image/gif"}
    MAX_IMAGE_COUNT: int = 10  # 이미지 최대 개수 제한 추가

    @classmethod
    def validate_images(cls, files: List[Any]) -> List[Any]:
        if not files:
            return files

        if len(files) > cls.MAX_IMAGE_COUNT:
            raise ValidationError(
                f"Cannot upload more than {cls.MAX_IMAGE_COUNT} images"
            )

        total_size = 0
        for image in files:
            # 파일 크기 검증
            if not hasattr(image, "size"):
                raise ValidationError("Invalid image file")

            total_size += image.size
            if image.size > cls.MAX_IMAGE_SIZE:
                raise ValidationError(
                    f"Image size cannot exceed {cls.MAX_IMAGE_SIZE // 1024 // 1024}MB"
                )

            # 파일 타입 검증
            if (
                not hasattr(image, "content_type")
                or image.content_type not in cls.ALLOWED_IMAGE_TYPES
            ):
                raise ValidationError(
                    f"Only {', '.join(cls.ALLOWED_IMAGE_TYPES)} are allowed"
                )

            # 이미지 파일이 깨졌는지 검증 (선택적)
            try:
                Image.open(image).verify()
            except Exception:
                raise ValidationError("Corrupted image file")

        return files

    def post(self, request: Request) -> Response:

        # 게시글 생성
        serializer = PostCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 이미지 유효성 검증
        images = self.validate_images(request.FILES.getlist("images"))

        # 게시글 생성
        post = PostService.create_post(
            user_id=request.user.id,
            data=serializer.validated_data,
            images=images,
        )

        # 응답
        return Response(
            PostDetailSerializer(post).data,
            status=status.HTTP_201_CREATED,
        )


class PostDetailView(APIView):
    # 게시글 상세 조회
    def get(self, request: Request, post_id: int) -> Response:
        # ETag 처리
        if_none_match = request.headers.get("If-None-Match")

        post = PostService.get_post_detail(
            post_id=post_id,
            user_id=request.user.id if request.user.is_authenticated else None,
        )

        context = {
            "request": request,
            "user_id": request.user.id if request.user.is_authenticated else None,
        }

        serializer = PostDetailSerializer(post, context=context)

        response = Response(serializer.data)
        response["Cache-Control"] = "max-age=60"

        return response


class PostUpdateView(APIView):
    def validate_image_operations(
        self, post_id: int, add_images: List[Any], remove_image_ids: List[int]
    ) -> None:
        # 삭제할 이미지가 해당 게시글의 것인지 확인
        if remove_image_ids:
            existing_images = set(
                PostImage.objects.filter(
                    post_id=post_id, id__in=remove_image_ids
                ).values_list("id", flat=True)
            )

            invalid_ids = set(remove_image_ids) - existing_images
            if invalid_ids:
                raise ValidationError(f"Invalid image IDs: {invalid_ids}")

    # 게시글 수정
    def patch(self, request: Request, post_id: int) -> Response:
        serializer = PostUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 이미지 작업 검증
        add_images = request.FILES.getlist("add_images")
        remove_image_ids = request.data.get("remove_image_ids", [])

        self.validate_image_operations(post_id, add_images, remove_image_ids)
        validated_images = PostCreateView.validate_images(add_images)  # 수정된 부분

        post = PostService.update_post(
            post_id=post_id,
            user_id=request.user.id,
            data=serializer.validated_data,
            add_image=validated_images,
            remove_image_ids=remove_image_ids,
        )

        return Response(PostDetailSerializer(post).data)


class PostDeleteView(APIView):
    # 게시글 삭제
    def delete(self, request: Request, post_id: int) -> Response:
        PostService.delete_post(post_id=post_id, user_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):
    # 게시글 좋아요
    @transaction.atomic
    def post(self, request: Request, post_id: int) -> Response:
        is_liked = PostService.toggle_like(
            post_id=post_id,
            user_id=request.user.id,
        )
        return Response({"is_liked": is_liked})
