from rest_framework.permissions import BasePermission


class UserIsOwnerTodo(BasePermission):

    def has_object_permission(self, request, view, user):
        return request.user.id == user.user.id
