from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer


# Leave Request List
# ------------------------------------------------------ 
class LeaveRequestListView(APIView):
    def get(self, request):
        leaves = get_list_or_404(LeaveRequest)
        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Leave Request Detail
# ------------------------------------------------------ 
class LeaveRequestDetailView(APIView):
    def get_object_helper(self, pk):
        '''Helper method to get leave request object by pk or raise 404 error otherwise'''
        return get_object_or_404(LeaveRequest, pk=pk)
    
    # Retrieve a single object by pk
    def get(self, request, pk):
        leave = self.get_object_helper(pk)        
        serializer = LeaveRequestSerializer(leave)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    def put(self, request, pk):
        leave = self.get_object_helper(pk)        
        serializer = LeaveRequestSerializer(leave, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    def delete(self, request, pk):
        leave = self.get_object_helper(pk)
        leave.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
