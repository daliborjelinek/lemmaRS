from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

from rs.models import Role


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            print('USER IS NOT AUTHENTICATED')
            return False

        if view.action == 'retrieve':
            return obj == request.user or request.user.role == Role.ADMIN or request.user.role == Role.PROVIDER
        elif view.action in ['update', 'partial_update']:
            return obj == request.user or request.user.is_admin
        else:
            return False


class ProjectPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(view.action)
        if view.action in ['update', 'partial_update', 'add_member', 'remove_member']:
            return obj.owner == request.user
        else:
            return request.user.is_authenticated


class ProjectGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == Role.ADMIN or
                                                  request.user.role == Role.PROVIDER or
                                                  request.method in SAFE_METHODS)


class ResourcePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == Role.ADMIN or
                                                  request.user.role == Role.PROVIDER or
                                                  request.method in SAFE_METHODS)


class PermissionLevelPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == Role.ADMIN or
                                                  request.user.role == Role.PROVIDER or
                                                  request.method in SAFE_METHODS)


class TagPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == Role.ADMIN or
                                                  request.user.role == Role.PROVIDER or
                                                  request.method in SAFE_METHODS)

