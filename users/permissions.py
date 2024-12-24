from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    사용자 본인만 접근할 수 있도록 하는 권한
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
