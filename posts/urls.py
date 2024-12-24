from django.urls import path

from posts.views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostLikeView,
    PostListView,
    PostUpdateView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<int:post_id>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:post_id>/update/", PostUpdateView.as_view(), name="post-update"),
    path("<int:post_id>/delete/", PostDeleteView.as_view(), name="post-delete"),
    # 좋아요
    path("<int:post_id>/like/", PostLikeView.as_view(), name="post-like"),
]
