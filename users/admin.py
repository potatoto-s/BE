# type: ignore
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    # role, workshop_name, company_name 필드를 추가
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {"fields": ("role", "workshop_name", "company_name")}),
    )
    # 유저 생성 시에도 해당 필드들이 보이도록
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {"fields": ("role", "workshop_name", "company_name")}),
    )
    # 리스트 화면에서도 해당 필드들이 보이도록
    list_display = (
        "username",
        "email",
        "role",
        "workshop_name",
        "company_name",
        "is_staff",
    )


admin.site.register(User, CustomUserAdmin)
