from rest_framework.permissions import BasePermission

# Admin Auth
# -------------------------------------
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff
    
# Manager Auth
# -------------------------------------
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == 'Manager'
    
# Employee Auth
# -------------------------------------
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'profile') and request.user.profile.role == 'Employee'