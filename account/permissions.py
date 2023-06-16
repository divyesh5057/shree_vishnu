from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        elif request.user.role == 'admin':
            return True
        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
