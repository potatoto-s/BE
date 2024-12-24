from django.urls import path

from comments.views import CommentCreateView, CommentDeleteView, CommentListView, CommentUpdateView

app_name = "comments"

urlpatterns = [
    # 댓글 목록 조회 - GET
    # /api/posts/{post_id}/comments/
    path("posts/<int:post_id>/comments/", CommentListView.as_view(), name="comment-list"),
    # 댓글 작성 - POST
    # /api/posts/{post_id}/comments/
    path(
        "posts/<int:post_id>/comments/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    # 댓글 수정 - PATCH
    # /api/comments/{comment_id}
    path(
        "<int:comment_id>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    # 댓글 삭제 - DELETE
    # /api/comments/{comment_id}/
    path(
        "<int:comment_id>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
