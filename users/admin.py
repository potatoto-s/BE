from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import User, EmailVerification


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = [
        'email',
        'nickname',
        'status_display',
        'location_display',
        'last_login_at',
        'profile_image_display'
    ]

    list_filter = [
        'status',
        'is_active',
        'is_staff',
        'district'
    ]

    search_fields = [
        'email',
        'nickname',
        'district',
        'neighborhood'
    ]

    readonly_fields = ['last_login_at', 'date_joined', 'status_changed_at']

    fieldsets = (
        ('계정 정보', {'fields': ('email', 'nickname', 'password')}),
        ('프로필', {'fields': ('profile_image', 'district', 'neighborhood', 'status')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('중요 일자', {'fields': ('last_login_at', 'date_joined')})
    )

    def status_display(self, obj):
        color_map = {'active': 'green', 'inactive': 'orange', 'suspended': 'red'}
        color = color_map.get(obj.status, 'black')
        return format_html('<span style="color: {};">{}</span>', color, obj.get_status_display())

    status_display.short_description = '상태'

    def location_display(self, obj):
        return f"{obj.district} {obj.neighborhood}" if obj.district and obj.neighborhood else "-"

    location_display.short_description = '활동 지역'

    def profile_image_display(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;"/>',
                obj.profile_image.url
            )
        return "이미지 없음"

    profile_image_display.short_description = '프로필 이미지'

    actions = ['activate_users', 'deactivate_users', 'suspend_users']

    def activate_users(self, request, queryset):
        queryset.update(status='active', status_changed_at=timezone.now())

    activate_users.short_description = '선택된 사용자 활성화'

    def deactivate_users(self, request, queryset):
        queryset.update(status='inactive', status_changed_at=timezone.now())

    deactivate_users.short_description = '선택된 사용자 비활성화'

    def suspend_users(self, request, queryset):
        queryset.update(status='suspended', status_changed_at=timezone.now())

    suspend_users.short_description = '선택된 사용자 이용 정지'


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'code',
        'verification_status',
        'created_at',
        'expires_at'
    ]

    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__email', 'code']
    readonly_fields = ['created_at', 'expires_at']

    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green;">인증됨</span>')
        if obj.is_expired():
            return format_html('<span style="color: red;">만료됨</span>')
        return format_html('<span style="color: orange;">대기중</span>')

    verification_status.short_description = '인증 상태'
