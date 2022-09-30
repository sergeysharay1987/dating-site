from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsUserPkInUrl(BasePermission):

    def has_permission(self, request, view):
        if view.action =='create':
            return True

    def has_object_permission(self, request, view, obj):
        if view.action in ['update', 'destroy']:
            return True
        return False


class AllowAnyCreate(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        # return False
