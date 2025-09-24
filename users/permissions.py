from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="managers").exists() or request.user.is_staff


class IsSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
