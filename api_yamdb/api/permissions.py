from rest_framework import permissions


class AdminOrReadOnlyPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.role is admin
            or request.user.is_superuser
        )


class AuthorAdminOrReadOnly(permissions.BasePermission):
    """Класс для контроля допуска пользователей."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.user.role in ('moderator', 'admin')
            or request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
        )
