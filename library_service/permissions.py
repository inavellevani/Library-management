from rest_framework import permissions


class IsEmployeePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsStaffOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser))