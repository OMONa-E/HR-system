import pytest
from applications.onboarding.models import Employee
from applications.attendance.models import Attendance
from datetime import datetime, timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# Attendance Model Test 
# ------------------------------
@pytest.mark.django_db
def test_create_attendance():
    employee = Employee.objects.create(
        employee_id = 'E1000',
        employee_nin = 'cm96lkgg8908dbn',
        full_name = 'Tester test',
        email = 'testertest@gmail.com',
        job_title = 'Engineer',
        phone_number = '256772484255',
    )
    attendance = Attendance.objects.create(
        employee=employee,
        clock_in_time=datetime(2024, 11, 26, 9, 0, tzinfo=timezone.utc),
        clock_out_time=datetime(2024, 11, 26, 17, 0, tzinfo=timezone.utc),
    )
    assert attendance.employee.full_name == 'Tester test'
    assert attendance.duration.total_seconds() == 8 * 3600

# # Attendance API POST GET URL Test 
# # -----------------------------------
# @pytest.mark.django_db
# def test_attendance_api():
#     client = APIClient()

#     # Create a test user
#     user = User.objects.create_user(username='testuser', password='testpass')

#     # Set the user's role to Admin
#     user.profile.role = 'Admin'
#     user.profile.save()

#     # Generate a valid JWT token for the user
#     refresh = RefreshToken.for_user(user)
#     access_token = str(refresh.access_token)

#     # Set the token in the Authorization header
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

#     # Create an employee
#     employee = Employee.objects.create(
#         employee_id='E1000',
#         employee_nin='cm96lkgg8908dbn',
#         full_name='Tester test',
#         email='testertest@gmail.com',
#         job_title='Engineer',
#         phone_number='256772484255',
#     )

#     # Make a POST request to the attendance logs endpoint
#     response = client.post("/api/attendance/logs/", {
#         "employee": employee.id,
#         "clock_in_time": "2024-11-26T09:00:00Z",
#         "clock_out_time": "2024-11-26T17:00:00Z",
#     })

#     assert response.status_code == 201
