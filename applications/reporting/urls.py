from django.urls import path
from .views import AttendanceReportView, LeaveReportView, EmployeeReportView, ExportEmployeeDataAsCSV, AttendanceFrequencyGraphView, LeaveStatusGraphView

urlpatterns = [
    path('employees/', EmployeeReportView.as_view(), name='employee-report'),
    path('attendance/', AttendanceReportView.as_view(), name='attendance-report'),
    path('leaves/', LeaveReportView.as_view(), name='leave-report'),
    path('export/employees/', ExportEmployeeDataAsCSV.as_view(), name='export-employees-csv'),
    path('graphs/attendance/', AttendanceFrequencyGraphView.as_view(), name='attendance-graph'),
    path('graphs/leaves/', LeaveStatusGraphView.as_view(), name='leave-status-graph'),
]
