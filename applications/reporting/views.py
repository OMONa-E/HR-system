import csv
from io import BytesIO
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from applications.onboarding.models import Employee
from applications.attendance.models import Attendance
from applications.leave_management.models import LeaveRequest



# Employee Report View
# -------------------------------------------------------------
class EmployeeReportView(APIView):
    def get(self, request):
        employees = get_list_or_404(Employee.objects.all().values('employee_id', 'employee_nin', 'full_name', 'email', 'job_title', 'phone_number', 'date_joined'))
        return Response(employees, status=status.HTTP_200_OK)
    
# Attendance Report View
# -------------------------------------------------------------
class AttendanceReportView(APIView):
    def get(self, request):
        logs = get_list_or_404(Attendance)
        log_data = [
            {
                'employee_name': log.employee.name,
                'clock_in_time': log.clock_in_time,
                'clock_out_time': log.clock_out_time,
                'duration': log.duration if log.clock_out_time else 'Empty',
            } for log in logs
        ]
        return Response(log_data, status=status.HTTP_200_OK)
    
# Leave Report View
# -------------------------------------------------------------
class LeaveReportView(APIView):
    def get(self, request):
        leaves = get_list_or_404(LeaveRequest.objects.all().values('employee__full_name', 'start_date', 'end_date', 'reason', 'status'))
        return Response(leaves, status=status.HTTP_200_OK)
    
# Export Employee As CSV View
# -------------------------------------------------------------
class ExportEmployeeDataAsCSV(APIView):
    def get(self, request):
        # Create the HttResponse object with CSV headers
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="employees.csv"'

        writer = csv.writer(response) # Create a CSV writer object
        writer.writerow(['Employee ID', 'Full Name', 'Email', 'Job Title', 'Date Joined']) # Write CSV headers
        employees = get_list_or_404(Employee)
        for employee in employees: 
            writer.writerow([employee.employee_id, employee.full_name, employee.email, employee.job_title, employee.date_joined]) # CSV body writing

        return response

# Attendance Frequency Graph View
# -------------------------------------------------------------   
class AttendanceFrequencyGraphView(APIView):
    def get(self, request):
        # Calculate attendance frequency
        employees = Attendance.objects.values_list('employee__full_name', flat=True).distinct()
        frequencies = [ Attendance.objects.filter(employee__full_name=name).count() for name in employees ]

        # Create a bar graph
        plt.figure(figsize=(12,6))
        plt.bar(employees, frequencies, color='blue')
        plt.xlabel('Employee Full Name', color='purple')
        plt.ylabel('Attendance Count', color='purple')
        plt.title('Employee Attendance Frequency Bar Graph', color='purple')
        plt.xticks(rotation=45)
        # Save the plot to a BytesIO object
        buffer = BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        # Return as an HTTP response
        return HttpResponse(buffer, content_type='image/png')
    
# Leave Status Graph View
# -------------------------------------------------------------   
class LeaveStatusGraphView(APIView):
    def get(self, request):
        # Calculate leave request status distribution        
        labels = ['Pending', 'Approved', 'Rejected']
        statuses = LeaveRequest.objects.values_list('status', flat=True)
        counts = [statuses.filter(status=status).count() for status in labels]

         # Validate data
        if not counts or any(c is None or c < 0 for c in counts):
            return Response({'error': 'Invalid data for pie chart'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Handle NaN or None values
        counts = np.nan_to_num(counts, nan=0.0)

        # Check for all-zero data
        if np.sum(counts) == 0:
            return Response({'error': 'No data to plot'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate pie chart
        try:
            plt.figure(figsize=(6, 6))
            plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
            plt.title('Leave Request Status Distribution')
            # Save the plot to a BytesIO object
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            plt.close()

            # Return the plot as a response
            return HttpResponse(buffer, content_type='image/png')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    