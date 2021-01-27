from rest_framework.permissions import BasePermission

from table.models import PermissionOnBoard, ColumnBoard, TaskColumn


# permission_types = (
#     (1, 'Owner'),
#     (2, 'Member'),
#     (3, 'Visitor'),
#     (4, 'Admin'),
# )

# class IsOwner(BasePermission):
#     def has_object_permission(self, request, view, obj: PermissionOnBoard):
#         return obj.permission == 1

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        return PermissionOnBoard.objects.filter(user=request.user.id, permission=1).exists()


class IsMember(BasePermission):
    def has_permission(self, request, view):
        return PermissionOnBoard.objects.filter(user=request.user.id, permission=2).exists()


class IsVisitor(BasePermission):
    def has_permission(self, request, view):
        return PermissionOnBoard.objects.filter(user=request.user.id, permission=3).exists()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return PermissionOnBoard.objects.filter(user=request.user.id, permission=4).exists()
