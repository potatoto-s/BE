from django.db import models

from users.models import User


class Post(models.Model):
    # 공방 사장만 작성 가능
    # 제목, 본문, 카테고리 필수 입력
    # 다중 이미지 업로드
    # 좋아요, 조회수, 댓글수
    # SOFT DELETE

    # 카테고리 별 필터링
    # 제목 / 본문 검색

    class Status(models.TextChoices):
        # 정상 게시 상태
        ACTIVE = "ACTIVE", "Active"
        # 숨김 상태
        HIDDEN = "HIDDEN", "Hidden"
        # 삭제된 상태
        DELETED = "DELETED", "Deleted"

    class Category(models.TextChoices):
        BALLOON = "BALLOON", "풍선/페이퍼아트"
        GIFT = "GIFT", "선물포장/보자기"
        WOOD = "WOOD", "목공/도자기/가죽"
        DIFFUSER = "DIFFUSER", "디퓨터/캔들/석고방향제"
        RESIN = "RESIN", "레진/비즈공예"
        RATTAN = "RATTAN", "라탄/마크라메"
        FLOWER = "FLOWER", "플라워"
        TOTAL = "TOTAL", "토탈공예"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255, help_text="게시글 제목")
    content = models.TextField(help_text="게시글 본문")
    category = models.CharField(
        max_length=20, choices=Category.choices, help_text="게시글 카테고리"
    )
    view_count = models.PositiveIntegerField(default=0, help_text="조회수")
    like_count = models.PositiveIntegerField(default=0, help_text="좋아요 수")
    comment_count = models.PositiveIntegerField(default=0, help_text="댓글 수")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        help_text="게시글 상태",
    )
    is_deleted = models.BooleanField(default=False, help_text="삭제 여부 (True인 경우 삭제)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="작성일시")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정일시")

    class Meta:
        db_table = "posts"
        ordering = ["-created_at"]
        indexes = [
            # 카테고리 검색 최적화
            models.Index(fields=["category"]),
            # 시간 순 정렬 최적화
            models.Index(fields=["created_at"]),
            # 삭제되지 않은 게시글 조회 최적화
            models.Index(fields=["is_deleted"]),
        ]

    def __str__(self) -> str:
        return self.title

    def delete(
        self, using: str | None = None, keep_parents: bool = False
    ) -> tuple[int, dict[str, int]]:
        # 소프트 딜리트 구현
        self.is_deleted = True
        self.save(using=using)

        # 원래 delete 메서드의 반환 형식을 맞추기 위해
        # (삭제된 객체 수, {모델명: 삭제된 객체수})의 형태로 반환
        return (1, {f"{self._meta.model_name}": 1})


class PostImage(models.Model):
    # 한 게시글 당 여러 이미지 업로드 가능
    # 게시글 삭제 시 이미지 삭제

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=2000, help_text="이미지 URL (유효한 URL 형식)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="업로드 일시")

    class Meta:
        db_table = "post_images"


class PostLike(models.Model):
    # 한 사용자 당 게시글 하나에 한 번 좋아요
    # 게시글 삭제 시 좋아요 삭제

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")
    created_at = models.DateTimeField(auto_now_add=True, help_text="좋아요 생성 일시")

    class Meta:
        db_table = "post_likes"
        # 사용자 당 게시글 하나에 한 번의 좋아요 가능
        unique_together = ["post", "user"]
