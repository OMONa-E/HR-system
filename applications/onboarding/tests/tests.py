from applications.onboarding.models import Employee
import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

# Employee Model Test 
# ------------------------------
@pytest.mark.django_db
def test_create_employee():
    employee = Employee.objects.create(
        employee_id = 'E1000',
        employee_nin = 'cm96lkgg8908dbn',
        full_name = 'Tester test',
        email = 'testertest@gmail.com',
        job_title = 'Engineer',
        phone_number = '256772484255',
    )
    assert employee.full_name == 'Tester test'
    assert employee.email == 'testertest@gmail.com'


# # Employee API POST GET URL Test 
# # -------------------------------------
# @pytest.mark.django_db
# def test_employee_api():
#     client = APIClient()

#     # Create a test user
#     user = User.objects.create_user(username='testuser', password='testpass')

#     # Set the user's role to Employee (default, but explicitly setting it here)
#     user.profile.role = 'Admin'
#     user.profile.save()

#     # Generate a valid JWT token for the user
#     refresh = RefreshToken.for_user(user)
#     access_token = str(refresh.access_token)

#     # Set the token in the Authorization header
#     client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

#     # Make a POST request to the employee onboarding endpoint
#     response = client.post("/api/onboarding/employees/", {
#         "employee_id": "E1000",
#         "employee_nin": "cm96lkgg8908dbn",
#         "full_name": "Tester test",
#         "email": "testertest@gmail.com",
#         "job_title": "Engineer",
#         "phone_number": "256772484255",
#     })

#     assert response.status_code == 201