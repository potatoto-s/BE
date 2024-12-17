from django.db import models


class Comment(models.Model):
    # 회원(기업/공방)만 작성 가능
    # 기업회원인 경우 기업명 표시
    # 공방회원인 경우 공방명 표시
    # 비회원 작성 불가
    # 내용 필수 입력
    # SOFT DELETE

    class Status(models.TextChoices):
        # 정상 상태
        ACTIVE = "ACTIVE", "Active"
        # 숨김 상태
        HIDDEN = "HIDDEN", "Hidden"
        # 삭제된 상태
        DELETED = "DELETED", "Deleted"
        
        
    post = models.ForeignKey("post.Post", on_delete=models.CASCADE, related_name="comments", help_text="댓글이 작성된 게시글")
    # User 모델 구현 후 수정
    user = models.ForeignKey("auth.User", ondelete=models.CASCADE, related_name="comments", help_text="댓글 작성자")
    content = models.TextField(help_text="댓글 내용")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, help_text="댓글 상태")
    created_at = models.DateTimeField(auto_now_add=True, help_text="작성일시")
    updated_at = models.DateTimeField(auto_now=True, help_text="수정일시")
    
    class Meta:
        db_table = "comments"
        ordering = ["-created_at"]
        indexes = [
            # 게시글 별 댓글 조회 최적화
            models.Index(fields=["post", "created_at"])
        ]
        
    def __str__(self) -> str:
        # 댓글 내용 앞 20자만 표시
        return f"{self.user}의 댓글 - {self.content[:20]}..."
    
    