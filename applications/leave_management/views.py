from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.auth.permissions import IsAdmin, IsManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from django.utils.decorators import method_decorator
from rest_framework.decorators import permission_classes


# Leave Request List
# ------------------------------------------------------ 
class LeaveRequestListView(APIView):
    """
    API view for listing and creating leave requests.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for both GET and POST methods.

    Methods:
        get(request):
            Retrieve a list of all leave requests.
            Returns:
                - HTTP 200: List of serialized leave requests.
                - HTTP 404: If no leave requests exist.
        post(request):
            Create a new leave request.
            Payload:
                - employee (int): The employee making the leave request.
                - start_date (date): The start date of the leave.
                - end_date (date): The end date of the leave.
                - reason (str): The reason for requesting leave.
            Returns:
                - HTTP 201: The created leave request.
                - HTTP 400: Validation errors.
    """
    serializer_class = LeaveRequestSerializer
    
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request):
        """
        Retrieve a list of all leave requests.

        Returns:
            - HTTP 200: List of serialized leave requests.
            - HTTP 404: If no leave requests exist.
        """
        leaves = get_list_or_404(LeaveRequest)
        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def post(self, request):
        """
        Create a new leave request.

        Payload:
            - employee (int): The employee making the leave request.
            - start_date (date): The start date of the leave.
            - end_date (date): The end date of the leave.
            - reason (str): The reason for requesting leave.

        Returns:
            - HTTP 201: The created leave request.
            - HTTP 400: Validation errors.
        """
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Leave Request Detail
# ------------------------------------------------------ 
class LeaveRequestDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a single leave request.

    Permissions:
        - Requires authentication (IsAuthenticated).
        - Admin and Manager roles are required for GET and PUT methods.
        - Admin role is required for DELETE method.

    Methods:
        get(request, pk):
            Retrieve a leave request by primary key.
            Returns:
                - HTTP 200: Serialized leave request.
                - HTTP 404: If the leave request does not exist.
        put(request, pk):
            Update a leave request by primary key.
            Payload:
                - start_date (date): The updated start date of the leave.
                - end_date (date): The updated end date of the leave.
                - reason (str): The updated reason for requesting leave.
            Returns:
                - HTTP 200: The updated leave request.
                - HTTP 400: Validation errors.
                - HTTP 404: If the leave request does not exist.
        delete(request, pk):
            Delete a leave request by primary key.
            Returns:
                - HTTP 204: No content, leave request successfully deleted.
                - HTTP 404: If the leave request does not exist.
    """
    serializer_class = LeaveRequestSerializer

    def get_object_helper(self, pk):
        """
        Helper method to retrieve a leave request object by primary key.

        Args:
            pk (int): The primary key of the leave request.

        Returns:
            LeaveRequest instance if found, otherwise raises HTTP 404.
        """
        return get_object_or_404(LeaveRequest, pk=pk)
    
    # Retrieve a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def get(self, request, pk):
        """
        Retrieve a leave request by primary key.

        Args:
            pk (int): The primary key of the leave request.

        Returns:
            - HTTP 200: Serialized leave request.
            - HTTP 404: If the leave request does not exist.
        """
        leave = self.get_object_helper(pk)        
        serializer = LeaveRequestSerializer(leave)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin, IsManager]))
    def put(self, request, pk):
        """
        Update a leave request by primary key.

        Args:
            pk (int): The primary key of the leave request.

        Payload:
            - start_date (date): The updated start date of the leave.
            - end_date (date): The updated end date of the leave.
            - reason (str): The updated reason for requesting leave.

        Returns:
            - HTTP 200: The updated leave request.
            - HTTP 400: Validation errors.
            - HTTP 404: If the leave request does not exist.
        """
        leave = self.get_object_helper(pk)        
        serializer = LeaveRequestSerializer(leave, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    @method_decorator(permission_classes([IsAuthenticated, IsAdmin]))
    def delete(self, request, pk):
        """
        Delete a leave request by primary key.

        Args:
            pk (int): The primary key of the leave request.

        Returns:
            - HTTP 204: No content, leave request successfully deleted.
            - HTTP 404: If the leave request does not exist.
        """
        leave = self.get_object_helper(pk)
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
