from django.urls import path

from .views import (
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostLikeView,
    PostListView,
    PostUpdateView,
)

app_name = "posts"

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:post_id>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:post_id>/update/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:post_id>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("posts/<int:post_id>/like/", PostLikeView.as_view(), name="post-like"),
]
