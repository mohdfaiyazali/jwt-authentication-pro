from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):

    def has_permission(self, request, view):

        return request.user.role == 'admin'


class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):

        return (
            obj.user == request.user
            or request.user.role == 'admin'
        )