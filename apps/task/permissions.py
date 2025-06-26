from rest_framework.permissions import BasePermission

class IsProjectOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "project_owner"

class IsProjectManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "project_manager"

class IsDeveloper(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "developer"

class IsTester(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "tester"

class IsProjectOwnerOrManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["project_owner", "project_manager"]

class IsAnyRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            "project_owner", "project_manager", "developer", "tester"
        ]