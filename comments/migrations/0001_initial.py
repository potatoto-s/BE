# Generated by Django 5.1.4 on 2025-01-02 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
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
                    models.BooleanField(default=False, help_text="삭제 여부 (True인 경우 삭제)"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, help_text="작성일시")),
                ("updated_at", models.DateTimeField(auto_now=True, help_text="수정일시")),
            ],
            options={
                "db_table": "comments",
                "ordering": ["-created_at"],
            },
        ),
    ]
