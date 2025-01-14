from django.urls import path

from .views import CommentCreateView, CommentDeleteView, CommentListView, CommentUpdateView

app_name = "comments"

urlpatterns = [
    path(
        "<int:post_id>/comments/",
        CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "<int:post_id>/comments/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "<int:comment_id>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "<int:comment_id>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
