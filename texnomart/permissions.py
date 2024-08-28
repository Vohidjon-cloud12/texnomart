
from rest_framework.permissions import BasePermission


class IsOwnerIsAuthenticated(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if obj.user == request.user or request.user.is_staff:
                return True
            return False


class IsSuperAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.is_staff:
                return True
            return False


