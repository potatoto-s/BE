# Generated by Django 5.1.4 on 2024-12-17 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("posts", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(help_text="댓글 내용")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ACTIVE", "Active"),
                            ("HIDDEN", "Hidden"),
                            ("DELETED", "Deleted"),
                        ],
                        default="ACTIVE",
                        help_text="댓글 상태",
                        max_length=20,
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(
                        default=False, help_text="삭제 여부 (True인 경우 삭제)"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, help_text="작성일시"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, help_text="수정일시"),
                ),
                (
                    "post",
                    models.ForeignKey(
                        help_text="댓글이 작성된 게시글",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="posts.post",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="댓글 작성자",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "comments",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["post", "created_at"],
                        name="comments_post_id_015fcc_idx",
                    ),
                    models.Index(
                        fields=["is_deleted"], name="comments_is_dele_5d074c_idx"
                    ),
                ],
            },
        ),
    ]