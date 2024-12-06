from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

# Helper Function
# -------------------------------------
def get_role(request):
    """
    Helper function to extract the user's role from a JWT token.

    This function validates the JWT token provided in the request's `Authorization` 
    header and extracts the user's role from the token payload.

    Args:
        request (Request): The incoming HTTP request containing the JWT token 
                           in the `Authorization` header.

    Returns:
        str: The role of the user as specified in the JWT token payload.
    
    Raises:
        AuthenticationFailed: If the token is invalid or missing.
        KeyError: If the role is not present in the token payload.
    
    Example Usage:
        role = get_role(request)
    """
    jwt_auth = JWTAuthentication()
    validated_token = jwt_auth.get_validated_token(request.headers.get("Authorization").split()[1])
    role = validated_token.get("role")
    return role

# Admin Auth
# -------------------------------------
class IsAdmin(BasePermission):
    """
    Custom permission class to check if the user has the 'Admin' role.

    This permission is used to restrict access to views or actions that 
    require the user to have administrative privileges.

    Methods:
        has_permission(request, view):
            Determines if the user has the 'Admin' role.

    Example:
        permission_classes = [IsAuthenticated, IsAdmin]

    Returns:
        bool: True if the user's role is 'Admin', False otherwise.
    """
    def has_permission(self, request, view):
        """
        Checks if the user's role is 'Admin'.

        Args:
            request (Request): The incoming HTTP request.
            view (View): The view being accessed.

        Returns:
            bool: True if the user's role is 'Admin', False otherwise.
        """
        role = get_role(request)
        print(f'{role}')
        return bool(role == 'Admin')
    
# Manager Auth
# -------------------------------------
class IsManager(BasePermission):
    """
    Custom permission class to check if the user has the 'Manager' role.

    This permission is used to restrict access to views or actions that 
    require the user to have managerial privileges.

    Methods:
        has_permission(request, view):
            Determines if the user has the 'Manager' role.

    Example:
        permission_classes = [IsAuthenticated, IsManager]

    Returns:
        bool: True if the user's role is 'Manager', False otherwise.
    """
    def has_permission(self, request, view):
        """
        Checks if the user's role is 'Manager'.

        Args:
            request (Request): The incoming HTTP request.
            view (View): The view being accessed.

        Returns:
            bool: True if the user's role is 'Manager', False otherwise.
        """
        role = get_role(request)
        role = get_role(request)
        print(f'{role}')
        return bool(role == 'Manager')
    
# Employee Auth
# -------------------------------------
class IsEmployee(BasePermission):
    """
    Custom permission class to check if the user has the 'Employee' role.

    This permission is used to restrict access to views or actions that 
    are specific to employees.

    Methods:
        has_permission(request, view):
            Determines if the user has the 'Employee' role.

    Example:
        permission_classes = [IsAuthenticated, IsEmployee]

    Returns:
        bool: True if the user's role is 'Employee', False otherwise.
    """
    def has_permission(self, request, view):
        """
        Checks if the user's role is 'Employee'.

        Args:
            request (Request): The incoming HTTP request.
            view (View): The view being accessed.

        Returns:
            bool: True if the user's role is 'Employee', False otherwise.
        """
        role = get_role(request)
        print(f'{role}')
        return bool(role == 'Employee')