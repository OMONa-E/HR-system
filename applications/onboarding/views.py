from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from core.auth.permissions import IsAdmin, IsManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Employee
from .serializers import EmployeeSerializer, UserSerializer


# User List API View
# --------------------------------------------
class UserListView(APIView):
    """
    API view for listing and creating user accounts.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for both GET and POST methods.

    Methods:
        get(request):
            Retrieve a list of all user accounts.
            Returns:
                - HTTP 200: List of serialized user accounts.
        post(request):
            Create a new user account.
            Payload:
                - username (str): The username of the user.
                - email (str): The email address of the user.
                - password (str): The password for the user account.
            Returns:
                - HTTP 201: The created user account.
                - HTTP 400: Validation errors.
    """
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request):
        """
        Retrieve a list of all user accounts.

        Returns:
            - HTTP 200: List of serialized user accounts.
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def post(self, request):
        """
        Create a new user account.

        Payload:
            - username (str): The username of the user.
            - email (str): The email address of the user.
            - password (str): The password for the user account.

        Returns:
            - HTTP 201: The created user account.
            - HTTP 400: Validation errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User Detail API View
# --------------------------------------------
class UserDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a single user account.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for GET and PUT methods.
        - Admin role is required for DELETE method.

    Methods:
        get(request, pk):
            Retrieve a user account by primary key.
            Returns:
                - HTTP 200: Serialized user account.
                - HTTP 404: If the user does not exist.
        put(request, pk):
            Update a user account by primary key.
            Payload:
                - username (str): Updated username of the user.
                - email (str): Updated email address of the user.
            Returns:
                - HTTP 200: The updated user account.
                - HTTP 400: Validation errors.
                - HTTP 404: If the user does not exist.
        delete(request, pk):
            Delete a user account by primary key.
            Returns:
                - HTTP 204: No content, user successfully deleted.
                - HTTP 404: If the user does not exist.
    """
    def get_object_helper(self, pk):
        """
        Helper method to retrieve a user account object by primary key.

        Args:
            pk (int): The primary key of the user account.

        Returns:
            User instance if found, otherwise raises HTTP 404.
        """
        return get_object_or_404(User, pk=pk)
    
    # Retrieve a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request, pk):
        """
        Retrieve a user account by primary key.

        Args:
            pk (int): The primary key of the user account.

        Returns:
            - HTTP 200: Serialized user account.
            - HTTP 404: If the user does not exist.
        """
        user = self.get_object_helper(pk)        
        serializer = UserWarning(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def put(self, request, pk):
        """
        Update a user account by primary key.

        Args:
            pk (int): The primary key of the user account.

        Payload:
            - username (str): Updated username of the user.
            - email (str): Updated email address of the user.

        Returns:
            - HTTP 200: The updated user account.
            - HTTP 400: Validation errors.
            - HTTP 404: If the user does not exist.
        """
        user = self.get_object_helper(pk)        
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin]))
    def delete(self, request, pk):
        """
        Delete a user account by primary key.

        Args:
            pk (int): The primary key of the user account.

        Returns:
            - HTTP 204: No content, user successfully deleted.
            - HTTP 404: If the user does not exist.
        """
        user = self.get_object_helper(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Employee List API View
# --------------------------------------------
class EmployeeListView(APIView):
    """
    API view for listing and creating employee records.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for both GET and POST methods.

    Methods:
        get(request):
            Retrieve a list of all employee records.
            Returns:
                - HTTP 200: List of serialized employee records.
        post(request):
            Create a new employee record.
            Payload:
                - Fields matching the EmployeeSerializer.
            Returns:
                - HTTP 201: The created employee record.
                - HTTP 400: Validation errors.
    """
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request):
        """
        Retrieve a list of all employee records.

        Returns:
            - HTTP 200: List of serialized employee records.
        """
        employees = get_list_or_404(Employee)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def post(self, request):
        """
        Create a new employee record.

        Payload:
            - Fields matching the EmployeeSerializer.

        Returns:
            - HTTP 201: The created employee record.
            - HTTP 400: Validation errors.
        """
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employee Detail API View
# --------------------------------------------
class EmployeeDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a single employee record.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for GET and PUT methods.
        - Admin role is required for DELETE method.

    Methods:
        get(request, pk):
            Retrieve an employee record by primary key.
            Returns:
                - HTTP 200: Serialized employee record.
                - HTTP 404: If the employee does not exist.
        put(request, pk):
            Update an employee record by primary key.
            Returns:
                - HTTP 200: The updated employee record.
                - HTTP 400: Validation errors.
                - HTTP 404: If the employee does not exist.
        delete(request, pk):
            Delete an employee record by primary key.
            Returns:
                - HTTP 204: No content, employee successfully deleted.
                - HTTP 404: If the employee does not exist.
    """
    def get_object_helper(self, pk):
        """
        Retrieve an employee record by primary key.

        Args:
            pk (int): The primary key of the employee record.

        Returns:
            - HTTP 200: Serialized employee record.
            - HTTP 404: If the employee does not exist.
        """
        return get_object_or_404(Employee, pk=pk)

    # Retrieve a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request, pk):
        """
        Retrieve an employee record by primary key.

        Args:
            pk (int): The primary key of the employee record.

        Returns:
            - HTTP 200: Serialized employee record.
            - HTTP 404: If the employee does not exist.
        """
        employee = self.get_object_helper(pk)        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def put(self, request, pk):
        """
        Update an employee record by primary key.

        Args:
            pk (int): The primary key of the employee record.

        Returns:
            - HTTP 200: The updated employee record.
            - HTTP 400: Validation errors.
            - HTTP 404: If the employee does not exist.
        """
        employee = self.get_object_helper(pk)        
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def delete(self, request, pk):
        """
        Delete an employee record by primary key.

        Args:
            pk (int): The primary key of the employee record.

        Returns:
            - HTTP 204: No content, employee successfully deleted.
            - HTTP 404: If the employee does not exist.
        """
        employee = self.get_object_helper(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)