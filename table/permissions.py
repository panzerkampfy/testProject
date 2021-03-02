from rest_framework.permissions import BasePermission

from table.models import PermissionOnBoard


# permission_types = (
#     (1, 'Owner'),
#     (2, 'Member'),
#     (3, 'Visitor'),
#     (4, 'Admin'),
# )


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj: PermissionOnBoard):
        if obj is None:
            return False
        return obj.permission == 1


class IsMember(BasePermission):
    def has_object_permission(self, request, view, obj: PermissionOnBoard):
        if obj is None:
            return False
        return obj.permission == 2


class IsVisitor(BasePermission):
    def has_object_permission(self, request, view, obj: PermissionOnBoard):
        if obj is None:
            return False
        return obj.permission == 3


class IsAdmin(BasePermission):
    def has_object_permission(self, request, view, obj: PermissionOnBoard):
        if obj is None:
            return False
        return obj.permission == 4
