from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.auth.permissions import IsAdmin, IsManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .serializers import AttendanceSerializer
from django.utils.decorators import method_decorator
from rest_framework.decorators import permission_classes


# Attendance List View
# ----------------------------------------------------
class AttendanceLogListView(APIView):
    """
    API view for listing and creating attendance logs.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for both GET and POST methods.

    Methods:
        get(request):
            Retrieve a list of all attendance logs.
            Returns:
                - HTTP 200: List of serialized attendance logs.
                - HTTP 404: If no logs exist.
        post(request):
            Create a new attendance log.
            Payload:
                - employee (int): The employee associated with the log.
                - clock_in_time (datetime): The clock-in time.
                - clock_out_time (datetime): The clock-out time.
            Returns:
                - HTTP 201: The created attendance log.
                - HTTP 400: Validation errors.
    """
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request):
        """
        Retrieve a list of all attendance logs.

        Returns:
            - HTTP 200: List of serialized attendance logs.
            - HTTP 404: If no logs exist.
        """
        logs = get_list_or_404(Attendance)
        serializer = AttendanceSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def post(self, request):
        """
        Create a new attendance log.

        Payload:
            - employee (int): The employee associated with the log.
            - clock_in_time (datetime): The clock-in time.
            - clock_out_time (datetime): The clock-out time.

        Returns:
            - HTTP 201: The created attendance log.
            - HTTP 400: Validation errors.
        """
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Attendance List View
# ----------------------------------------------------
class AttendanceLogDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a single attendance log.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for GET and PUT methods.
        - Admin role is required for DELETE method.

    Methods:
        get(request, pk):
            Retrieve an attendance log by primary key.
            Returns:
                - HTTP 200: Serialized attendance log.
                - HTTP 404: If the log does not exist.
        put(request, pk):
            Update an attendance log by primary key.
            Payload:
                - employee (int): The employee associated with the log.
                - clock_in_time (datetime): The clock-in time.
                - clock_out_time (datetime): The clock-out time.
            Returns:
                - HTTP 200: The updated attendance log.
                - HTTP 400: Validation errors.
                - HTTP 404: If the log does not exist.
        delete(request, pk):
            Delete an attendance log by primary key.
            Returns:
                - HTTP 204: No content, log successfully deleted.
                - HTTP 404: If the log does not exist.
    """
    def get_object_helper(self, pk):
        """
        Helper method to retrieve an attendance log object by primary key.

        Args:
            pk (int): The primary key of the attendance log.

        Returns:
            Attendance instance if found, otherwise raises HTTP 404.
        """
        return get_object_or_404(Attendance, pk=pk)
    
    # Retrieve a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request, pk):
        """
        Retrieve an attendance log by primary key.

        Args:
            pk (int): The primary key of the attendance log.

        Returns:
            - HTTP 200: Serialized attendance log.
            - HTTP 404: If the log does not exist.
        """
        log = self.get_object_helper(pk)        
        serializer = AttendanceSerializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def put(self, request, pk):
        """
        Update an attendance log by primary key.

        Args:
            pk (int): The primary key of the attendance log.

        Payload:
            - employee (int): The employee associated with the log.
            - clock_in_time (datetime): The clock-in time.
            - clock_out_time (datetime): The clock-out time.

        Returns:
            - HTTP 200: The updated attendance log.
            - HTTP 400: Validation errors.
            - HTTP 404: If the log does not exist.
        """
        log = self.get_object_helper(pk)        
        serializer = AttendanceSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin]))
    def delete(self, request, pk):
        """
        Delete an attendance log by primary key.

        Args:
            pk (int): The primary key of the attendance log.

        Returns:
            - HTTP 204: No content, log successfully deleted.
            - HTTP 404: If the log does not exist.
        """
        log = self.get_object_helper(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)