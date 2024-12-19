from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post

User = get_user_model()


class PostTests(APITestCase):
    # 게시글 관련 테스트

    def setUp(self) -> None:
        # 테스트 데이터 설정
        # 공방 사장 계정 생성
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            role="WORKSHOP",
            email="test@test.com",  # email 추가
        )
        self.client.force_authenticate(user=self.user)

        # 테스트용 게시글 생성
        self.post = Post.objects.create(
            user=self.user,
            title="Test Post",
            content="Test Content" * 3,
            category="FLOWER",
        )

    def test_create_post(self) -> None:
        # 게시글 작성 테스트
        # url = "/api/posts/create/"
        url = reverse("posts:post-create")

        data = {
            "title": "New Test Post",
            "content": "New Test Content" * 3,
            "category": "FLOWER",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_post_with_short_content(self) -> None:
        # 최소 길이 미달 내용 테스트
        url = "/api/posts/create/"
        data = {
            "title": "Test Post",
            "content": "Short",
            "category": "FLOWER",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_list(self) -> None:
        # 게시글 목록 조회 테스트
        # url = "/api/posts/"
        url = reverse("posts:post-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

    def test_post_detail(self) -> None:
        # 게시글 상세 조회 테스트
        # url = f"/api/posts/{self.post.id}/"
        url = reverse("posts:post-detail", kwargs={"post_id": self.post.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")

    def test_update_post(self) -> None:
        # 게시글 수정 테스트
        url = f"/api/posts/{self.post.id}/update/"
        data = {
            "title": "Updated Post",
            "content": "Updated Content" * 3,
        }

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post.id).title, "Updated Post")

    def test_delete_post(self) -> None:
        # 게시글 삭제 테스트
        url = f"/api/posts/{self.post.id}/delete/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Post.objects.get(id=self.post.id).is_deleted)

    def test_post_like(self) -> None:
        # 게시글 좋아요 테스트
        url = f"/api/posts/{self.post.id}/like/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_liked"])
