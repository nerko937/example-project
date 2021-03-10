from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'Only owners are allowed to edit.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # model must have owner field
        return obj.owner == request.user
