from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.user.role == 'admin'
            or request.method in permissions.SAFE_METHODS
        )


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or obj.author == request.user
