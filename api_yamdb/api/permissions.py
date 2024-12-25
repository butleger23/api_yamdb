from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Разрешаем доступ для администраторов
        if request.user.is_staff:
            return True

        # Разрешаем доступ для получения данных
        if view.action in ['list', 'retrieve']:
            return True

        # Запрещаем доступ для cоздания объектов обычным пользователям
        if view.action == 'create':
            return request.user.is_staff

        # Запрещаем доступ для удаления объектов обычным пользователям
        if view.action == 'destroy':
            return request.user.is_staff
        return False
