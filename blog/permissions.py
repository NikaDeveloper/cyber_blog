from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """ Разрешает редактирование только себе или администратору """
    def has_object_permission(self, request, view, obj):
        # админ всегда имеет доступ
        if request.user and request.user.is_staff:
            return True

        # если объект это сам пользователь (для UserViewSet)
        if hasattr(obj, 'username'):
            return obj == request.user

        # если у объекта есть автор (для Post, Comment)
        return getattr(obj, 'author', None) == request.user
