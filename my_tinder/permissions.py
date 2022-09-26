from rest_framework.permissions import BasePermission


class IsUserPkInUrl(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.id == obj.id and view.action == 'update':
            return True
        return False
