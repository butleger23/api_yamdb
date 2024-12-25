from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем доступ для администраторов
        if request.user.is_staff or request.user.role == 'admin':
            return True

        # Разрешаем доступ для модераторов к созданию и удалению объектов
        if request.user.role == 'admin' and view.action in ['create', 'destroy']:
            return True

        # Разрешаем доступ для получения данных
        if view.action in ['list', 'retrieve']:
            return True

        return False
