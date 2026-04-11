from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """ Разрешает редактирование только себе или администратору """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if hasattr(obj, 'username'):
            return obj == request.user

        return obj.author == request.user
