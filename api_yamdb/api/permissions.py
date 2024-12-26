from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем доступ для администраторов
        if request.user.is_staff or request.user.role == 'admin':
            return True

        # Разрешаем доступ для безопасных методов (чтение)
        return request.method in permissions.SAFE_METHODS


class AuthorOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        return request.method == 'GET' or obj.author == request.user
