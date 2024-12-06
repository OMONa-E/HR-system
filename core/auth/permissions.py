from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

# Helper Function
# -------------------------------------
def get_role(request):
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(request.headers.get("Authorization").split()[1])
    role = validated_token.get("role")
    return role

# Admin Auth
# -------------------------------------
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        role = get_role(request)
        print(f'{role}')
        return bool(role == 'Admin')
    
# Manager Auth
# -------------------------------------
class IsManager(BasePermission):
    def has_permission(self, request, view):
        role = get_role(request)
        print(f'{role}')
        return bool(role == 'Manager')
    
# Employee Auth
# -------------------------------------
class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        role = get_role(request)
        print(f'{role}')
        return bool(role == 'Employee')