from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        COMPANY = "COMPANY", "Company"
        WORKSHOP = "WORKSHOP", "Workshop"
        GUEST = "GUEST", "Guest"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.GUEST,
    )
    company_name = models.CharField(max_length=255, blank=True)
    workshop_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "users"
