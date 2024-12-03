from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer


# Employee List API View
# --------------------------------------------
class EmployeeListView(APIView):
    def get(self, request):
        employees = get_list_or_404(Employee)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Employee Detail API View
# --------------------------------------------
class EmployeeDetailView(APIView):
    def get_object_helper(self, pk):
        '''Helper method to get an employee object by pk or raise 404 error otherwise'''
        return get_object_or_404(Employee, pk=pk)

    # Retrieve a single object by pk
    def get(self, request, pk):
        employee = self.get_object_helper(pk)        
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a single object by pk
    def put(self, request, pk):
        employee = self.get_object_helper(pk)        
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete a single object by pk
    def delete(self, request, pk):
        employee = self.get_object_helper(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)