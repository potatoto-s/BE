from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment
from posts.models import Post

User = get_user_model()


class CommentTests(APITestCase):
    # 댓글 관련 테스트

    def setUp(self) -> None:
        # 테스트 데이터 설정
        # 테스트 사용자 생성 (기업 회원)
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            role="COMPANY",
            email="test@test.com",
        )

        # 공방 사장님 생성 (게시글 작성용)
        self.workshop_user = User.objects.create_user(
            username="workshop",
            password="testpass123",
            role="WORKSHOP",
            email="workshop@test.com",
        )

        # 테스트용 게시글 생성
        self.post = Post.objects.create(
            user=self.workshop_user,
            title="Test Post",
            content="Test Content" * 3,
            category="FLOWER",
        )

        # 테스트용 댓글 생성
        self.comment = Comment.objects.create(
            post=self.post,
            user=self.user,
            content="Test Comment",
        )

    def test_create_comment(self) -> None:
        # 댓글 작성 테스트
        self.client.force_authenticate(user=self.user)
        url = reverse("comments:comment-create", kwargs={"post_id": self.post.id})
        data = {"content": "Test Comment"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_without_auth(self) -> None:
        # 비로그인 상태에서 댓글 작성 시도
        url = reverse("comments:comment-create", kwargs={"post_id": self.post.id})
        data = {"content": "Test Comment"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_comments(self) -> None:
        # 댓글 목록 조회 테스트
        url = reverse("comments:comment-list", kwargs={"post_id": self.post.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_update_comment(self) -> None:
        # 댓글 수정 테스트
        self.client.force_authenticate(user=self.user)
        url = reverse("comments:comment-update", kwargs={"comment_id": self.comment.id})
        data = {"content": "Updated Comment"}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Comment.objects.get(id=self.comment.id).content, "Updated Comment"
        )

    def test_delete_comment(self) -> None:
        # 댓글 삭제 테스트
        self.client.force_authenticate(user=self.user)
        url = reverse("comments:comment-delete", kwargs={"comment_id": self.comment.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Comment.objects.get(id=self.comment.id).is_deleted)
