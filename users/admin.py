from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "name", "nickname", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("email", "name", "nickname")
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인정보", {"fields": ("name", "nickname", "phone")}),
        ("권한", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("소속정보", {"fields": ("company_name", "workshop_name")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "nickname",
                    "phone",
                    "role",
                    "company_name",
                    "workshop_name",
                ),
            },
        ),
    )
