from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    class Meta:
        db_table = 'users'
        verbose_name = '사용자'
        verbose_name_plural = '사용자 목록'
        ordering = ['-created_at']
