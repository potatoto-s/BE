from django.urls import path

from .views import CommentCreateView, CommentDeleteView, CommentListView, CommentUpdateView

app_name = "comments"

urlpatterns = [
    path(
        "posts/<int:post_id>/comments/",
        CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "posts/<int:post_id>/comments/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comments/<int:comment_id>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comments/<int:comment_id>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
