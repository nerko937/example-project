from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = 'Only owners are allowed to edit.'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # model must have owner field
        return obj.owner == request.user


class IsIssueOwner(permissions.BasePermission):
    message = 'Only issue owners are allowed to delete.'

    def has_object_permission(self, request, view, obj):
        # model must have issue fk with owner field
        return obj.issue.owner == request.user
