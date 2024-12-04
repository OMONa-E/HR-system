from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.auth.permissions import IsAdmin, IsManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Attendance
from .serializers import AttendanceSerializer


# Attendance List View
# ----------------------------------------------------
class AttendanceLogListView(APIView):
    def get(self, request):
        self.permission_classes = [IsAuthenticated, IsAdmin, IsManager]
        self.check_permissions(request)

        logs = get_list_or_404(Attendance)
        serializer = AttendanceSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        self.permission_classes = [IsAuthenticated, IsAdmin, IsManager]
        self.check_permissions(request)

        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Attendance List View
# ----------------------------------------------------
class AttendanceLogDetailView(APIView):
    def get_object_helper(self, pk):
        '''Helper method to get an attendance log object by pk or raise 404 error otherwise'''
        return get_object_or_404(Attendance, pk=pk)
    
    # Retrieve a single object by pk
    def get(self, request, pk):
        self.permission_classes = [IsAuthenticated, IsAdmin, IsManager]
        self.check_permissions(request)

        log = self.get_object_helper(pk)        
        serializer = AttendanceSerializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    def put(self, request, pk):
        self.permission_classes = [IsAuthenticated, IsAdmin, IsManager]
        self.check_permissions(request)

        log = self.get_object_helper(pk)        
        serializer = AttendanceSerializer(log, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    def delete(self, request, pk):
        self.permission_classes = [IsAuthenticated, IsAdmin]
        self.check_permissions(request)

        log = self.get_object_helper(pk)
        log.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)